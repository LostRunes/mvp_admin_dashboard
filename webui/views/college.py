"""College PYQ & YT: YouTube links, Subject & Branch manager, College JSON importer."""
import streamlit as st

from webui import jobs
from webui.importers import import_college_json, parse_json_upload
from webui.services import (clear_college_caches, friendly_error, load_branches, load_subjects,
                            load_years, subject_label, supabase)
from webui.ui import flash, log_action, page_header

FILTERS = ["ALL", "WITH LINKS", "WITHOUT LINKS"]


def _reset(keys):
    for k in keys:
        st.session_state.pop(k, None)


def render():
    page_header("🎥  College PYQ & YT Link Uploader", "yt")
    try:
        subjects, branches, years = load_subjects(), load_branches(), load_years()
    except Exception as e:
        st.error(f"Could not load data from Supabase: {friendly_error(e)}")
        return

    t1, t2, t3 = st.tabs(["YouTube Links", "Subject & Branch", "JSON Importer"])
    with t1:
        _tab_youtube(subjects)
    with t2:
        _tab_subject_branch(branches, years)
    with t3:
        _tab_import(subjects)


def _tab_youtube(subjects):
    with st.container(border=True):
        mode = st.segmented_control("Subject Filter", FILTERS, default="ALL", required=True, key="yt_filter") or "ALL"
        filtered = [s for s in subjects
                    if mode == "ALL"
                    or (mode == "WITH LINKS" and (s.get("yt_links") or []))
                    or (mode == "WITHOUT LINKS" and not (s.get("yt_links") or []))]
        if not filtered:
            st.info("No subjects match this filter.")
            return
        s = st.selectbox("Subject", filtered, format_func=subject_label, key=f"yt_sub_{mode}")

    with st.container(border=True):
        links = "\n".join(s.get("yt_links") or [])
        # Keyed by subject + current DB value so switching subject / saving reloads the box
        txt = st.text_area("YouTube Lecture URLs (one per line)", value=links, height=260,
                           key=f"yt_links_{s['id']}_{hash(links)}")
        if st.button("💾  Save YouTube Links", type="primary"):
            urls = [ln.strip() for ln in txt.split("\n") if ln.strip()]
            bad = [u for u in urls if not u.lower().startswith(("http://", "https://"))]
            if bad:
                st.error("Each line must be a full http(s) link. Invalid: " + ", ".join(bad[:5]))
                return
            try:
                supabase().table("subjects").update({"yt_links": urls}).eq("id", s["id"]).execute()
                log_action("SAVE_YT_LINKS", content_type="yt_links", subject=s.get("name"),
                           content_id=s["id"], details={"count": len(urls)})
                clear_college_caches()
                flash("YouTube links saved successfully!")
                st.rerun()
            except Exception as e:
                st.error(friendly_error(e))


def _tab_subject_branch(branches, years):
    with st.container(border=True):
        st.markdown("**Add New Subject**")
        sn = st.text_input("Subject Name", key="ns_name", placeholder="Subject Name")
        sc = st.text_input("Subject Code", key="ns_code", placeholder="Subject Code")
        sp = st.text_input("PYQ Drive Link", key="ns_pyq")
        sno = st.text_input("Notes Drive Link", key="ns_notes")
        sco = st.text_input("Course Outcome Link", key="ns_co")
        st.markdown("**Map New Subject To branch/year/sem**")
        c1, c2, c3 = st.columns(3)
        br = c1.selectbox("Branch", branches, format_func=lambda b: b["name"], key="ns_branch")
        yr = c2.selectbox("Year", years, format_func=lambda y: y["name"], key="ns_year")
        sem = c3.selectbox("Semester", list(range(1, 9)), key="ns_sem")

        if st.button("✚  CREATE SUBJECT & MAP", type="primary"):
            s_name, s_code = sn.strip(), sc.strip()
            if not s_name or not s_code:
                st.warning("Subject Name and Code are required.")
            elif not br or not yr:
                st.warning("Add a branch and a year first (below), then map the subject.")
            else:
                _create_subject(s_name, s_code, sp.strip() or None, sno.strip() or None,
                                sco.strip() or None, br, yr, sem)

    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Add New Branch**")
            bn = st.text_input("Branch name", key="nb_name", label_visibility="collapsed",
                               placeholder="e.g. Computer Science")
            if st.button("✚  ADD BRANCH"):
                _simple_insert("branches", bn, "Branch", "nb_name")
        with c2:
            st.markdown("**Add New Year**")
            yn = st.text_input("Year name", key="ny_name", label_visibility="collapsed",
                               placeholder="e.g. 2026-2027")
            if st.button("✚  ADD YEAR"):
                _simple_insert("years", yn, "Year", "ny_name")


def _create_subject(name, code, pyq, notes, co, br, yr, sem):
    sb = supabase()
    try:
        res = sb.table("subjects").insert({
            "name": name, "code": code, "pyq_drive_link": pyq,
            "notes_drive_link": notes, "course_outcome_link": co,
        }).execute()
    except Exception as e:
        st.error(friendly_error(e))
        return
    if not res.data:
        st.error("Subject was not created (no row returned).")
        return
    sid = res.data[0]["id"]
    try:
        sb.table("branch_subjects").insert({
            "branch_id": br["id"], "subject_id": sid, "year_id": yr["id"], "semester": int(sem)
        }).execute()
    except Exception as e:
        # Don't leave an unmapped subject behind
        try:
            sb.table("subjects").delete().eq("id", sid).execute()
        except Exception:
            pass
        st.error(f"Mapping failed, subject creation rolled back: {friendly_error(e)}")
        return
    log_action("CREATE_SUBJECT", content_type="subject", subject=name, content_id=sid,
               details={"code": code, "branch": br["name"], "year": yr["name"], "semester": int(sem)})
    clear_college_caches()
    _reset(["ns_name", "ns_code", "ns_pyq", "ns_notes", "ns_co"])
    flash(f"Subject '{name}' created!")
    st.rerun()


def _simple_insert(table, raw, label, key):
    n = (raw or "").strip()
    if not n:
        st.warning(f"Enter a {label.lower()} name.")
        return
    try:
        res = supabase().table(table).insert({"name": n}).execute()
    except Exception as e:
        st.error(friendly_error(e))
        return
    log_action(f"CREATE_{label.upper()}", content_type=table, subject=n,
               content_id=(res.data or [{}])[0].get("id"))
    clear_college_caches()
    _reset([key])
    flash(f"{label} '{n}' created!")
    st.rerun()


def _tab_import(subjects):
    running = jobs.is_running("college_import")
    with st.container(border=True):
        st.markdown("**Import Questions JSON**")
        if not subjects:
            st.info("No subjects yet — create one in the Subject & Branch tab.")
            return
        s = st.selectbox("Target subject", subjects, format_func=subject_label, key="cj_sub",
                         disabled=running)
        up = st.file_uploader("Choose PYQ JSON File", type=["json"], key="cj_file", disabled=running)
        if st.button("📂  Upload & Import JSON", type="primary", disabled=running or not up):
            try:
                data = parse_json_upload(up.getvalue())
            except ValueError as e:
                st.error(str(e))
            else:
                log_action("IMPORT_COLLEGE_JSON", content_type="college_json", subject=s.get("name"),
                           content_id=s["id"], file_name=up.name)
                jobs.start_job("college_import", import_college_json, supabase(), s["id"], data)
                st.rerun()
    with st.container(border=True):
        jobs.render_job_log("college_import", "Import logs")
