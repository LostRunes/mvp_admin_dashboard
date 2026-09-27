"""College solution image uploader + GATE question/option image uploader.

Mirrors the standalone question_img_uploader / gate_img_uploader tools (the dashboard's
own .exe versions called a non-existent ImageKit method and non-existent columns).
"""
import streamlit as st

from webui.services import (friendly_error, imagekit_upload, load_branches, natural_key,
                            subject_label, supabase, validate_image)
from webui.ui import flash, log_action, page_header


# ── shared helpers ────────────────────────────────────────────────────────────
def _pick(label, options, key, fmt=str):
    """Selectbox that shows a disabled '-' when there is nothing to choose (like the desktop)."""
    if not options:
        st.selectbox(label, ["-"], key=f"{key}__empty", disabled=True)
        return None
    return st.selectbox(label, options, key=key, format_func=fmt)


def _thumbs(sources, cols=3, width=150):
    grid = st.columns(cols)
    for i, src in enumerate(sources):
        grid[i % cols].image(src, width=width)


def _replace_images(table: str, fk_col: str, fk_val, urls: list[str]):
    """Swap the image rows for one question/option; restore the old rows if the insert fails."""
    sb = supabase()
    old = sb.table(table).select("*").eq(fk_col, fk_val).execute().data or []
    sb.table(table).delete().eq(fk_col, fk_val).execute()
    try:
        sb.table(table).insert([
            {fk_col: fk_val, "image_url": u, "order_index": i} for i, u in enumerate(urls, 1)
        ]).execute()
    except Exception:
        if old:
            try:
                sb.table(table).insert(old).execute()
            except Exception:
                pass
        raise


def _upload_all(files, folder: str, prefix: str) -> list[str]:
    validated = [validate_image(f) for f in files]           # fail fast before uploading anything
    urls = []
    prog = st.progress(0.0, text="Uploading…")
    for i, ((data, ext), f) in enumerate(zip(validated, files), 1):
        prog.progress((i - 1) / len(files), text=f"Uploading {f.name} to ImageKit ({i}/{len(files)})…")
        urls.append(imagekit_upload(data, f"{prefix}{i}{ext}", folder))
    prog.progress(1.0, text="Saving to database…")
    return urls


def _bump(key):
    st.session_state[key] = st.session_state.get(key, 0) + 1


# ══════════════════════════════════════════════════════════════════════════════
# College solution images
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=60, show_spinner=False)
def _c_semesters(branch_id):
    r = supabase().table("branch_subjects").select("semester").eq("branch_id", branch_id).execute()
    return sorted({x["semester"] for x in r.data if x.get("semester") is not None})


@st.cache_data(ttl=60, show_spinner=False)
def _c_subjects(branch_id, sem):
    r = (supabase().table("branch_subjects").select("subject_id, subjects(id, name, code)")
         .eq("branch_id", branch_id).eq("semester", sem).execute())
    seen, out = set(), []
    for row in r.data:
        s = row.get("subjects")
        if s and s["id"] not in seen:
            seen.add(s["id"])
            out.append(s)
    return sorted(out, key=lambda x: (x.get("name") or "").lower())


@st.cache_data(ttl=60, show_spinner=False)
def _c_years(subject_id):
    r = supabase().table("pyq_sources").select("year").eq("subject_id", subject_id).execute()
    return sorted({x["year"] for x in r.data if x.get("year") is not None}, reverse=True)


@st.cache_data(ttl=60, show_spinner=False)
def _c_exams(subject_id, year):
    r = supabase().table("pyq_sources").select("exam_type").eq("subject_id", subject_id).eq("year", year).execute()
    return sorted({x["exam_type"] for x in r.data if x.get("exam_type") is not None})


@st.cache_data(ttl=60, show_spinner=False)
def _c_seasons(subject_id, year, exam):
    r = (supabase().table("pyq_sources").select("season").eq("subject_id", subject_id)
         .eq("year", year).eq("exam_type", exam).execute())
    return sorted({x["season"] for x in r.data if x.get("season") is not None})


@st.cache_data(ttl=60, show_spinner=False)
def _c_questions(subject_id, year, exam, season):
    r = (supabase().table("pyq_sources").select("id, question_number").eq("subject_id", subject_id)
         .eq("year", year).eq("exam_type", exam).eq("season", season).execute())
    return sorted(r.data or [], key=lambda q: natural_key(q.get("question_number")))


@st.cache_data(ttl=60, show_spinner=False)
def _c_question(pyq_source_id):
    r = (supabase().table("question_pyq_map").select("question_id, questions(question_text)")
         .eq("pyq_source_id", pyq_source_id).execute())
    if not r.data:
        return None
    row = r.data[0]
    return {"question_id": row["question_id"],
            "question_text": (row.get("questions") or {}).get("question_text") or "No text description."}


@st.cache_data(ttl=30, show_spinner=False)
def _c_existing(question_id):
    return (supabase().table("images").select("*").eq("question_id", question_id)
            .order("order_index").execute().data or [])


def render_college():
    page_header("🖼️  College Solution Image Uploader", "college_img")
    left, right = st.columns(2, gap="medium")
    sel = None
    try:
        with left, st.container(border=True):
            br = _pick("Branch", load_branches(), "ci_branch", lambda b: b["name"])
            sem = _pick("Semester", _c_semesters(br["id"]) if br else [], f"ci_sem_{br and br['id']}")
            subj = _pick("Subject", _c_subjects(br["id"], sem) if sem is not None else [],
                         f"ci_sub_{br and br['id']}_{sem}", subject_label)
            sid = subj["id"] if subj else None
            yr = _pick("Year", _c_years(sid) if sid else [], f"ci_yr_{sid}")
            ex = _pick("Exam Type", _c_exams(sid, yr) if yr is not None else [], f"ci_ex_{sid}_{yr}")
            sea = _pick("Season", _c_seasons(sid, yr, ex) if ex else [], f"ci_sea_{sid}_{yr}_{ex}")
            qs = _c_questions(sid, yr, ex, sea) if sea else []
            q = _pick("Question", qs, f"ci_q_{sid}_{yr}_{ex}_{sea}", lambda x: str(x["question_number"]))
            if q:
                sel = _c_question(q["id"])
            st.text_area("Question Text Preview:", value=(sel or {}).get("question_text", "")
                         if sel else ("⚠ No question is linked to this PYQ entry." if q else ""),
                         height=180, disabled=True, key=f"ci_prev_{q and q['id']}")
    except Exception as e:
        st.error(f"Could not load data from Supabase: {friendly_error(e)}")
        return

    with right, st.container(border=True):
        if sel:
            existing = _c_existing(sel["question_id"])
            st.caption(f"Currently {len(existing)} solution image(s) saved for this question.")
            if existing:
                with st.expander("View current images"):
                    _thumbs([x["image_url"] for x in existing])
        v = st.session_state.get("ci_up_v", 0)
        files = st.file_uploader("📸  Choose Images", type=["png", "jpg", "jpeg", "webp"],
                                 accept_multiple_files=True, key=f"ci_files_{v}")
        if files:
            st.caption("Upload order = order shown here (1, 2, 3 …)")
            _thumbs(files, width=110)
        if sel:
            st.info(f"Target: **{br['name']} · Sem {sem} · {subject_label(subj)} · {yr} · {ex} · "
                    f"{sea} · Q{q['question_number']}** — existing images will be replaced.")
        if st.button("🚀  Upload solution images to cloud", type="primary", width="stretch"):
            if not sel:
                st.warning("Select a question first.")
            elif not files:
                st.warning("No images selected.")
            else:
                qid = sel["question_id"]
                try:
                    urls = _upload_all(files, f"images/{qid}", "")
                    _replace_images("images", "question_id", qid, urls)
                except Exception as e:
                    st.error(f"Upload failed: {friendly_error(e)}")
                    return
                log_action("UPLOAD_COLLEGE_IMAGES", content_type="college_solution_images",
                           subject=subj.get("name"), content_id=qid,
                           details={"count": len(urls), "question_number": str(q["question_number"])})
                _c_existing.clear()
                _bump("ci_up_v")
                flash(f"{len(urls)} image(s) uploaded successfully!")
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# GATE question / option images
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=60, show_spinner=False)
def _g_years():
    r = supabase().table("gate_papers").select("year").execute()
    return sorted({x["year"] for x in r.data if x.get("year") is not None}, reverse=True)


@st.cache_data(ttl=60, show_spinner=False)
def _g_papers(year):
    r = supabase().table("gate_papers").select("*").eq("year", year).execute()
    return sorted(r.data or [], key=lambda p: (p.get("exam") or "", p.get("set_number") or 0))


@st.cache_data(ttl=60, show_spinner=False)
def _g_paper_questions(paper_id):
    r = (supabase().table("gate_question_occurrences")
         .select("question_id, question_number, gate_questions(id, question_text, subject_id, gate_subjects(id, name))")
         .eq("paper_id", paper_id).execute())
    out = []
    for row in r.data:
        gq = row.get("gate_questions")
        if gq:
            out.append({"question_id": row["question_id"], "question_number": row["question_number"],
                        "question_text": gq.get("question_text") or "No text description.",
                        "subject_id": gq.get("subject_id"),
                        "subject_name": (gq.get("gate_subjects") or {}).get("name") or "Unknown subject"})
    return sorted(out, key=lambda q: natural_key(q["question_number"]))


@st.cache_data(ttl=30, show_spinner=False)
def _g_options(question_id):
    r = supabase().table("gate_options").select("id, option_label").eq("question_id", question_id).execute()
    return sorted(r.data or [], key=lambda o: o.get("option_label") or "")


@st.cache_data(ttl=30, show_spinner=False)
def _g_existing(table, fk_col, fk_val):
    return (supabase().table(table).select("*").eq(fk_col, fk_val).order("order_index").execute().data or [])


def _paper_label(p):
    return f"{p.get('exam')} (Set {p.get('set_number')})"


def render_gate():
    page_header("📐  GATE Image Asset Uploader", "gate_img")
    left, right = st.columns(2, gap="medium")
    q = target = None
    try:
        with left, st.container(border=True):
            yr = _pick("Year", _g_years(), "gi_yr")
            pap = _pick("Paper", _g_papers(yr) if yr is not None else [], f"gi_pap_{yr}", _paper_label)
            pqs = _g_paper_questions(pap["id"]) if pap else []
            subjects = sorted({(x["subject_id"], x["subject_name"]) for x in pqs}, key=lambda s: s[1])
            sub = _pick("Subject", subjects, f"gi_sub_{pap and pap['id']}", lambda s: s[1])
            qs = [x for x in pqs if sub and x["subject_id"] == sub[0]]
            q = _pick("Question", qs, f"gi_q_{pap and pap['id']}_{sub and sub[0]}",
                      lambda x: str(x["question_number"]))
            if q:
                opts = _g_options(q["question_id"])
                targets = [("question", None, "Question Body")] + \
                          [("option", o["id"], f"Option {o['option_label']}") for o in opts]
                target = st.selectbox("Target component", targets, format_func=lambda t: t[2],
                                      key=f"gi_tgt_{q['question_id']}")
            st.text_area("Question Text Preview:", value=q["question_text"] if q else "", height=180,
                         disabled=True, key=f"gi_prev_{q and q['question_id']}")
    except Exception as e:
        st.error(f"Could not load data from Supabase: {friendly_error(e)}")
        return

    with right, st.container(border=True):
        if q and target:
            table, fk, fk_val = (("gate_question_images", "question_id", q["question_id"])
                                 if target[0] == "question" else ("gate_option_images", "option_id", target[1]))
            existing = _g_existing(table, fk, fk_val)
            st.caption(f"Currently {len(existing)} image(s) saved for {target[2]}.")
            if existing:
                with st.expander("View current images"):
                    _thumbs([x["image_url"] for x in existing])
        v = st.session_state.get("gi_up_v", 0)
        files = st.file_uploader("📂  Select Image(s)", type=["png", "jpg", "jpeg", "webp"],
                                 accept_multiple_files=True, key=f"gi_files_{v}")
        if files:
            _thumbs(files, width=110)
        else:
            st.caption("No image selected.")
        if q and target:
            st.info(f"Target: **{yr} · {_paper_label(pap)} · {sub[1]} · Q{q['question_number']} · "
                    f"{target[2]}** — existing images will be replaced.")
        if st.button("🚀  Upload Image", type="primary", width="stretch"):
            if not q or not target:
                st.warning("Select a question first.")
            elif not files:
                st.warning("Select an image file.")
            else:
                try:
                    if target[0] == "question":
                        urls = _upload_all(files, f"gate/questions/{q['question_id']}", "q_")
                        _replace_images("gate_question_images", "question_id", q["question_id"], urls)
                    else:
                        urls = _upload_all(files, f"gate/options/{target[1]}", "opt_")
                        _replace_images("gate_option_images", "option_id", target[1], urls)
                except Exception as e:
                    st.error(f"Upload failed: {friendly_error(e)}")
                    return
                log_action("UPLOAD_GATE_IMAGES", content_type=f"gate_{target[0]}_images",
                           subject=sub[1], content_id=target[1] or q["question_id"],
                           details={"count": len(urls), "target": target[2],
                                    "question_number": str(q["question_number"])})
                _g_existing.clear()
                _bump("gi_up_v")
                flash("GATE asset image(s) uploaded successfully!")
                st.rerun()
