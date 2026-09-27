"""Protected GATE question database editor."""
import hmac
import string
import threading
import time
import uuid

import streamlit as st

from webui.config import get_secret
from webui.services import friendly_error, supabase
from webui.ui import flash, log_action, page_header

MAX_ATTEMPTS = 5
LOCKOUT_SECONDS = 300
DIFFICULTIES = ["easy", "medium", "hard"]
QTYPES = ["MCQ", "NAT", "MSQ"]


@st.cache_resource
def _attempts() -> dict:
    """Server-wide failed-attempt counter per account (survives page reloads)."""
    return {"lock": threading.Lock(), "by_user": {}}


def _gate(email: str) -> bool:
    if st.session_state.get("gdb_unlocked"):
        return True
    pw = get_secret("ADMIN_PASSWORD")
    if not pw:
        st.error("🔒 ADMIN_PASSWORD is not configured on the server, so the editor stays locked.")
        return False
    store = _attempts()
    with store["lock"]:
        fails, until = store["by_user"].get(email, (0, 0.0))
    if time.time() < until:
        st.error(f"🔒 Too many wrong attempts. Try again in {int(until - time.time()) + 1} s.")
        return False

    with st.container(border=True):
        st.markdown("### 🔒 Protected Area\nAdmin Access Required. Enter admin password:")
        with st.form("gdb_pw", clear_on_submit=True):
            entry = st.text_input("Admin password", type="password")
            ok = st.form_submit_button("Unlock", type="primary")
    if ok:
        if hmac.compare_digest(entry.encode("utf-8"), str(pw).encode("utf-8")):
            with store["lock"]:
                store["by_user"].pop(email, None)
            st.session_state.gdb_unlocked = True
            log_action("UNLOCK_GATE_DB", content_type="gate_db")
            st.rerun()
        fails += 1
        until = time.time() + LOCKOUT_SECONDS if fails >= MAX_ATTEMPTS else 0.0
        with store["lock"]:
            store["by_user"][email] = (0 if until else fails, until)
        log_action("UNLOCK_GATE_DB_FAILED", content_type="gate_db")
        st.error("Incorrect password." + (" Editor locked for 5 minutes." if until else
                                          f" {MAX_ATTEMPTS - fails} attempt(s) left."))
    return False


@st.cache_data(ttl=60, show_spinner=False)
def _subjects():
    return supabase().table("gate_subjects").select("id,name").order("name").execute().data or []


@st.cache_data(ttl=30, show_spinner=False)
def _questions(subject_id):
    return (supabase().table("gate_questions")
            .select("id,question_text,difficulty,marks,question_type,explanation")
            .eq("subject_id", subject_id).execute().data or [])


def _load_into_editor(qid):
    sb = supabase()
    q = sb.table("gate_questions").select("id,subject_id,question_text,difficulty,marks,question_type,explanation") \
        .eq("id", qid).execute().data
    if not q:
        st.session_state.pop("gdb_edit", None)
        flash("That question no longer exists.", "warning")
        return
    opts = sb.table("gate_options").select("id,option_label,option_text,is_correct") \
        .eq("question_id", qid).execute().data or []
    opts.sort(key=lambda o: o.get("option_label") or "")
    st.session_state.gdb_edit = {
        "qid": qid, "q": q[0], "v": uuid.uuid4().hex[:8],
        "opts": [{"uid": uuid.uuid4().hex[:8], "id": o["id"], "label": o.get("option_label") or "",
                  "text": o.get("option_text") or "", "correct": bool(o.get("is_correct"))} for o in opts],
    }


def render(email: str):
    page_header("🎓  Protected GATE Question Database Editor", "gate_db")
    if not _gate(email):
        return
    try:
        subjects = _subjects()
    except Exception as e:
        st.error(f"Could not load subjects: {friendly_error(e)}")
        return

    left, right = st.columns([1, 1.2], gap="medium")
    with left, st.container(border=True):
        if not subjects:
            st.info("No GATE subjects in the database yet.")
            return
        subj = st.selectbox("Select Subject", subjects, format_func=lambda s: s["name"], key="gdb_sub")
        search = st.text_input("Search", placeholder="Search question body text...", key="gdb_search")
        try:
            qs = _questions(subj["id"])
        except Exception as e:
            st.error(friendly_error(e))
            return
        needle = search.strip().lower()
        shown = [q for q in qs if not needle or needle in (q.get("question_text") or "").lower()]
        st.caption(f"{len(shown)} of {len(qs)} question(s)")
        cur = (st.session_state.get("gdb_edit") or {}).get("qid")
        with st.container(height=560, border=False):
            for q in shown:
                txt = " ".join((q.get("question_text") or "").split())
                if st.button(txt[:55] + "...", key=f"gdb_q_{q['id']}", width="stretch",
                             type="primary" if q["id"] == cur else "secondary"):
                    _load_into_editor(q["id"])
                    st.rerun()

    with right, st.container(border=True):
        ed = st.session_state.get("gdb_edit")
        if ed and ed["q"].get("subject_id") != subj["id"]:
            ed = None      # selection belongs to another subject
        if not ed:
            st.info("Click a question on the left to edit it.")
            return
        _editor(ed, subj)


def _editor(ed, subj):
    q, k = ed["q"], f"gdb_{ed['qid']}_{ed['v']}"
    txt = st.text_area("Question Text Body:", value=q.get("question_text") or "", height=160, key=f"{k}_txt")
    exp = st.text_area("Explanation:", value=q.get("explanation") or "", height=120, key=f"{k}_exp")
    c1, c2, c3 = st.columns(3)
    diffs = DIFFICULTIES + ([q["difficulty"]] if q.get("difficulty") and q["difficulty"] not in DIFFICULTIES else [])
    types = QTYPES + ([q["question_type"]] if q.get("question_type") and q["question_type"] not in QTYPES else [])
    diff = c1.selectbox("Difficulty", diffs, index=diffs.index(q.get("difficulty") or "easy"), key=f"{k}_diff")
    qtype = c2.selectbox("Type", types, index=types.index(q.get("question_type") or "MCQ"), key=f"{k}_type")
    marks = c3.text_input("Marks", value=str(q.get("marks") or 1), key=f"{k}_marks")

    st.markdown("**Options Manager**")
    for o in list(ed["opts"]):
        ok_ = f"{k}_o_{o['uid']}"
        a, b, c, d = st.columns([0.8, 5, 1.6, 0.8], vertical_alignment="bottom")
        o["label"] = a.text_input("Label", value=o["label"], key=f"{ok_}_l", label_visibility="collapsed")
        o["text"] = b.text_input("Text", value=o["text"], key=f"{ok_}_t", label_visibility="collapsed",
                                 placeholder="Option text")
        o["correct"] = c.selectbox("Correct", ["False", "True"], index=int(o["correct"]), key=f"{ok_}_c",
                                   label_visibility="collapsed") == "True"
        if o["id"]:
            with d.popover("🗑"):
                st.write("Delete this option from the database now?")
                if st.button("Delete", key=f"{ok_}_del", type="primary"):
                    try:
                        supabase().table("gate_options").delete().eq("id", o["id"]).execute()
                    except Exception as e:
                        st.error(friendly_error(e))
                    else:
                        ed["opts"].remove(o)
                        log_action("DELETE_GATE_OPTION", content_type="gate_option",
                                   subject=subj["name"], content_id=o["id"])
                        st.rerun()
        elif d.button("🗑", key=f"{ok_}_rm"):
            ed["opts"].remove(o)
            st.rerun()

    if st.button("➕  Add Option"):
        used = {o["label"] for o in ed["opts"]}
        nxt = next((ch for ch in string.ascii_uppercase if ch not in used), "A")
        ed["opts"].append({"uid": uuid.uuid4().hex[:8], "id": None, "label": nxt, "text": "", "correct": False})
        st.rerun()

    st.divider()
    s1, s2 = st.columns(2)
    if s1.button("💾  Save Changes", type="primary", width="stretch"):
        _save(ed, subj, txt, exp, diff, qtype, marks)
    if s2.button("🗑  Delete Question", width="stretch"):
        _confirm_delete(ed["qid"], subj["name"])


def _save(ed, subj, txt, exp, diff, qtype, marks):
    try:
        marks_i = int(str(marks).strip())
    except ValueError:
        st.error("Marks must be a whole number.")
        return
    if not txt.strip():
        st.error("Question text cannot be empty.")
        return
    if any(not o["label"].strip() for o in ed["opts"]):
        st.error("Every option needs a label (A, B, C …).")
        return
    qid, sb = ed["qid"], supabase()
    try:
        sb.table("gate_questions").update({
            "question_text": txt, "explanation": exp, "difficulty": diff,
            "marks": marks_i, "question_type": qtype,
        }).eq("id", qid).execute()
        for o in ed["opts"]:
            row = {"option_label": o["label"].strip(), "option_text": o["text"], "is_correct": o["correct"]}
            if o["id"]:
                sb.table("gate_options").update(row).eq("id", o["id"]).execute()
            else:
                res = sb.table("gate_options").insert({"question_id": qid, **row}).execute()
                if res.data:
                    o["id"] = res.data[0]["id"]      # so a second save doesn't insert it again
    except Exception as e:
        st.error(f"Save failed: {friendly_error(e)}")
        return
    log_action("EDIT_GATE_QUESTION", content_type="gate_question", subject=subj["name"], content_id=qid,
               details={"options": len(ed["opts"])})
    _questions.clear()
    _load_into_editor(qid)
    flash("GATE Question changes saved successfully!")
    st.rerun()


@st.dialog("Delete?")
def _confirm_delete(qid, subject_name):
    st.write("Delete this question permanently? Its options, images, topic links and paper "
             "occurrences are removed too.")
    c1, c2 = st.columns(2)
    if c1.button("Yes, delete", type="primary", width="stretch"):
        try:
            _delete_question(qid)
        except Exception as e:
            st.error(friendly_error(e))
            return
        log_action("DELETE_GATE_QUESTION", content_type="gate_question", subject=subject_name, content_id=qid)
        st.session_state.pop("gdb_edit", None)
        _questions.clear()
        flash("Question deleted.")
        st.rerun()
    if c2.button("Cancel", width="stretch"):
        st.rerun()


def _delete_question(qid):
    sb = supabase()
    opt_ids = [o["id"] for o in (sb.table("gate_options").select("id").eq("question_id", qid).execute().data or [])]
    if opt_ids:
        sb.table("gate_option_images").delete().in_("option_id", opt_ids).execute()
    sb.table("gate_options").delete().eq("question_id", qid).execute()
    for table in ("gate_question_images", "gate_question_topics", "gate_question_occurrences"):
        sb.table(table).delete().eq("question_id", qid).execute()
    sb.table("gate_questions").delete().eq("id", qid).execute()
