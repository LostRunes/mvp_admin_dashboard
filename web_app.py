import os
import json
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="☕ FocusFox Admin Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Glassmorphism Theme)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1C1B29 0%, #0F0E17 100%);
        color: #E8E2FF;
    }
    .stCard {
        background: rgba(40, 36, 68, 0.7);
        border: 1px solid #5C53A3;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #8174D6;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #F3A6C3;
        color: #1C1B29;
    }
</style>
""", unsafe_allow_html=True)

# Supabase Initialization
@st.cache_resource
def get_supabase_client():
    from supabase import create_client
    url = os.getenv("SUPABASE_URL") or st.secrets.get("SUPABASE_URL", "https://hoihnpzdlivaoywrshmk.supabase.co")
    key = os.getenv("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvaWhucHpkbGl2YW95d3JzaG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzczMDc1MjAsImV4cCI6MjA5Mjg4MzUyMH0.0XavqpSZjXVvuVRdEvI1Iy7ZGCOxCfGBA0cROVHyvHI")
    return create_client(url, key)

supabase = get_supabase_client()

# Sidebar Navigation
st.sidebar.title("☕ FocusFox Admin")
st.sidebar.caption("Web Management Portal")

page = st.sidebar.radio(
    "Navigation",
    ["📖 User Guide", "📹 YouTube Links", "📚 Subject & Branch", "📥 College PYQ Importer", "🎓 GATE Admin"]
)

# Helper Functions
def load_subjects():
    res = supabase.table("subjects").select("id, name, code, yt_links, pyq_drive_link, notes_drive_link, course_outcome_link").order("name").execute()
    return res.data or []

def load_branches():
    res = supabase.table("branches").select("id, name").order("name").execute()
    return res.data or []

def load_years():
    res = supabase.table("years").select("id, name").order("name").execute()
    return res.data or []

# ── 1. USER GUIDE PAGE ────────────────────────────────────────────────────────
if page == "📖 User Guide":
    st.title("📖 Developer User Guide & Database Schema")
    st.info("Welcome to the FocusFox Admin Web Portal! Use the sidebar navigation to manage subjects, YouTube links, and upload PYQ JSON data.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📚 College Admin Guide")
        st.write("""
        - **YouTube Links**: Associate video lecture playlists with subjects.
        - **Subject & Branch**: Register new courses and map them to branches, years, and semesters.
        - **JSON Importer**: Upload structured question banks extracted from course PYQs.
        """)
    with col2:
        st.subheader("🎓 GATE Admin Guide")
        st.write("""
        - **GATE Importer**: Seed official GATE syllabus, chapters, paper occurrences, and question options directly into Supabase.
        """)

# ── 2. YOUTUBE LINKS MANAGER ──────────────────────────────────────────────────
elif page == "📹 YouTube Links":
    st.title("📹 YouTube Lecture Links Manager")
    subjects = load_subjects()
    if not subjects:
        st.warning("No subjects found in database.")
    else:
        subject_map = {f"{s['name']} ({s['code']})": s for s in subjects}
        selected_sub_name = st.selectbox("Select Subject", list(subject_map.keys()))
        selected_sub = subject_map[selected_sub_name]
        
        current_links = selected_sub.get("yt_links") or []
        links_text = st.text_area(
            "YouTube Playlists / Video Links (One link per line)",
            value="\n".join(current_links),
            height=200
        )
        
        if st.button("💾 Save YouTube Links"):
            new_links = [l.strip() for l in links_text.split("\n") if l.strip()]
            supabase.table("subjects").update({"yt_links": new_links}).eq("id", selected_sub["id"]).execute()
            st.success(f"Successfully updated YouTube links for '{selected_sub['name']}'!")

# ── 3. SUBJECT & BRANCH CREATOR ───────────────────────────────────────────────
elif page == "📚 Subject & Branch":
    st.title("📚 Subject & Branch Manager")
    
    tab1, tab2, tab3 = st.tabs(["➕ Create Subject", "🌿 Create Branch", "📅 Create Year"])
    
    with tab1:
        s_name = st.text_input("Subject Name (e.g. Operating Systems)")
        s_code = st.text_input("Subject Code (e.g. CS30001)")
        pyq_l = st.text_input("PYQ Drive Link")
        note_l = st.text_input("Notes Drive Link")
        co_l = st.text_input("Course Outcome Link")
        
        branches = load_branches()
        years = load_years()
        
        b_name = st.selectbox("Branch", [b["name"] for b in branches]) if branches else None
        y_name = st.selectbox("Year", [y["name"] for y in years]) if years else None
        sem_val = st.selectbox("Semester", list(range(1, 9)))
        
        if st.button("➕ Create Subject & Map"):
            if not s_name or not s_code:
                st.error("Subject Name and Code are required!")
            else:
                res_s = supabase.table("subjects").insert({
                    "name": s_name, "code": s_code,
                    "pyq_drive_link": pyq_l or None,
                    "notes_drive_link": note_l or None,
                    "course_outcome_link": co_l or None
                }).execute()
                if res_s.data:
                    sid = res_s.data[0]["id"]
                    br_obj = next((b for b in branches if b["name"] == b_name), None)
                    yr_obj = next((y for y in years if y["name"] == y_name), None)
                    if br_obj and yr_obj:
                        supabase.table("branch_subjects").insert({
                            "branch_id": br_obj["id"],
                            "subject_id": sid,
                            "year_id": yr_obj["id"],
                            "semester": sem_val
                        }).execute()
                    st.success(f"Subject '{s_name}' created and mapped successfully!")

    with tab2:
        b_new = st.text_input("New Branch Name (e.g. Computer Science)")
        if st.button("➕ Add Branch"):
            if b_new:
                supabase.table("branches").insert({"name": b_new}).execute()
                st.success(f"Branch '{b_new}' created!")

    with tab3:
        y_new = st.text_input("New Year Name (e.g. 2026-2027)")
        if st.button("➕ Add Year"):
            if y_new:
                supabase.table("years").insert({"name": y_new}).execute()
                st.success(f"Year '{y_new}' created!")

# ── 4. COLLEGE PYQ JSON IMPORTER ──────────────────────────────────────────────
elif page == "📥 College PYQ Importer":
    st.title("📥 College PYQ JSON Importer")
    
    subjects = load_subjects()
    if not subjects:
        st.warning("No subjects available.")
    else:
        subject_map = {f"{s['name']} ({s['code']})": s for s in subjects}
        selected_sub_name = st.selectbox("Select Target Subject for JSON", list(subject_map.keys()))
        selected_sub = subject_map[selected_sub_name]
        
        uploaded_file = st.file_uploader("Choose PYQ JSON File", type=["json"])
        
        if uploaded_file and st.button("🚀 Upload & Import JSON"):
            try:
                data = json.load(uploaded_file)
                topics = data.get("topics", [])
                qs = data.get("questions", [])
                
                st.write(f"Importing **{len(topics)} topics** and **{len(qs)} questions**...")
                progress_bar = st.progress(0)
                status_log = st.empty()
                
                # Insert Topics
                tm = {}
                for t in topics:
                    r = supabase.table("topics").insert({
                        "subject_id": selected_sub["id"],
                        "name": t["topic_name"],
                        "summary": t.get("summary")
                    }).execute()
                    if r.data:
                        tm[t["topic_name"]] = r.data[0]["id"]
                
                # Insert Questions
                for i, q in enumerate(qs):
                    rq = supabase.table("questions").insert({
                        "question_text": q["question_text"],
                        "difficulty": q.get("difficulty", "easy")
                    }).execute()
                    if rq.data:
                        qid = rq.data[0]["id"]
                        for tn in q.get("topics", []):
                            tid = tm.get(tn)
                            if tid:
                                supabase.table("question_topics").insert({"question_id": qid, "topic_id": tid}).execute()
                        for src in q.get("pyq_sources", []):
                            ex = supabase.table("pyq_sources").select("id").match({**src, "subject_id": selected_sub["id"]}).execute()
                            pid = ex.data[0]["id"] if ex.data else (
                                supabase.table("pyq_sources").insert({**src, "subject_id": selected_sub["id"]}).execute().data or [{}]
                            )[0].get("id")
                            if pid:
                                supabase.table("question_pyq_map").insert({"question_id": qid, "pyq_source_id": pid}).execute()
                    progress_bar.progress((i + 1) / len(qs))
                    status_log.text(f"Processed question {i+1} of {len(qs)}")
                
                st.success("✅ Import Completed Successfully!")
            except Exception as e:
                st.error(f"Import failed: {e}")

# ── 5. GATE ADMIN & IMPORTER ──────────────────────────────────────────────────
elif page == "🎓 GATE Admin":
    st.title("🎓 GATE Admin & JSON Importer")
    
    uploaded_gate_file = st.file_uploader("Choose GATE JSON File", type=["json"])
    
    if uploaded_gate_file and st.button("🚀 Import GATE JSON"):
        try:
            data = json.load(uploaded_gate_file)
            sd = data.get("subject", {})
            topics = data.get("topics", [])
            qs = data.get("questions", [])
            
            rs = supabase.table("gate_subjects").select("*").eq("code", sd.get("subject_code")).execute()
            if rs.data:
                sid = rs.data[0]["id"]
            else:
                ri = supabase.table("gate_subjects").insert({
                    "name": sd.get("subject_name"), "code": sd.get("subject_code"), "display_order": 0
                }).execute()
                sid = ri.data[0]["id"]
                
            tm = {}
            for t in topics:
                rt = supabase.table("gate_topics").select("id").match({"subject_id": sid, "name": t["topic_name"]}).execute()
                if rt.data:
                    tm[t["topic_name"]] = rt.data[0]["id"]
                else:
                    ri = supabase.table("gate_topics").insert({"subject_id": sid, "name": t["topic_name"], "summary": t.get("summary")}).execute()
                    if ri.data:
                        tm[t["topic_name"]] = ri.data[0]["id"]
                        
            progress_bar = st.progress(0)
            status_log = st.empty()
            
            for i, q in enumerate(qs):
                rq = supabase.table("gate_questions").insert({
                    "subject_id": sid, "question_text": q["question_text"],
                    "explanation": q.get("explanation"), "question_type": q.get("question_type", "MCQ"),
                    "marks": q.get("marks", 1), "difficulty": q.get("difficulty", "easy")
                }).execute()
                if rq.data:
                    qid = rq.data[0]["id"]
                    for tn in q.get("topics", []):
                        tid = tm.get(tn)
                        if tid:
                            supabase.table("gate_question_topics").insert({"question_id": qid, "topic_id": tid}).execute()
                    for opt in q.get("options", []):
                        supabase.table("gate_options").insert({
                            "question_id": qid, "option_label": opt.get("label"),
                            "option_text": opt.get("text"), "is_correct": opt.get("is_correct", False)
                        }).execute()
                    for src in q.get("pyq_sources", []):
                        rp = supabase.table("gate_papers").select("id").match({
                            "exam": src.get("exam", "GATE CSE"), "year": src["year"], "set_number": src.get("set")
                        }).execute()
                        pid = rp.data[0]["id"] if rp.data else (
                            supabase.table("gate_papers").insert({
                                "exam": src.get("exam", "GATE CSE"), "year": src["year"], "set_number": src.get("set")
                            }).execute().data or [{}]
                        )[0].get("id")
                        if pid:
                            supabase.table("gate_question_occurrences").insert({
                                "question_id": qid, "paper_id": pid, "question_number": src["question_number"]
                            }).execute()
                progress_bar.progress((i + 1) / len(qs))
                status_log.text(f"Processed GATE question {i+1} of {len(qs)}")
                
            st.success("✅ GATE Import Complete!")
        except Exception as e:
            st.error(f"GATE Import failed: {e}")
