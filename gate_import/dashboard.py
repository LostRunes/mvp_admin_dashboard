import streamlit as st
import os
import json
import base64
import zipfile
from io import BytesIO
from pypdf import PdfReader, PdfWriter
import requests

# Set page config
st.set_page_config(
    page_title="GATE PYQ Admin Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# Supabase Integration Helpers
# -------------------------------------------------------------
# Try importing config/supabase_utils directly. If not possible, look up env variables.
try:
    from config import SUPABASE_URL, SUPABASE_KEY, HEADERS
    import supabase_utils
except ImportError:
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    HEADERS = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

def get_supabase_client_info():
    return SUPABASE_URL, HEADERS

def test_supabase_connection():
    if not SUPABASE_URL or not SUPABASE_KEY:
        return False
    try:
        url = f"{SUPABASE_URL}/rest/v1/gate_subjects?limit=1"
        res = requests.get(url, headers=HEADERS)
        return res.status_code == 200
    except Exception:
        return False

# Custom DB query helper functions using PostgREST directly (safer and fully customizable)
def db_select(table, params=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.get(url, headers=HEADERS, params=params)
    if res.status_code != 200:
        st.error(f"Error fetching {table}: {res.text}")
        return []
    return res.json()

def db_insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.post(url, headers=HEADERS, json=data)
    if res.status_code not in (200, 201):
        st.error(f"Error inserting into {table}: {res.text}")
        return None
    return res.json()

def db_update(table, data, match_params):
    # Match params should be structured as query params
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.patch(url, headers=HEADERS, json=data, params=match_params)
    if res.status_code not in (200, 204):
        st.error(f"Error updating {table}: {res.text}")
        return False
    return True

def db_delete(table, match_params):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    res = requests.delete(url, headers=HEADERS, params=match_params)
    if res.status_code not in (200, 204):
        st.error(f"Error deleting from {table}: {res.text}")
        return False
    return True

# -------------------------------------------------------------
# Main Premium styling using customized Markdown and CSS
# -------------------------------------------------------------
st.markdown("""
    <style>
    .main-header {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.8rem;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        padding: 1.5rem;
        border: 1px solid #f0f0f0;
        margin-bottom: 1rem;
    }
    .sidebar-header {
        font-weight: 700;
        font-size: 1.2rem;
        color: #1e3c72;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-header'>🎓 GATE Portal Admin</div>", unsafe_allow_html=True)
section = st.sidebar.radio(
    "Navigate to",
    ["🥞 PDF Splitter", "📥 JSON Importer", "🔐 Question Database Editor (Protected)"]
)

# -------------------------------------------------------------
# SECTION 1: PDF SPLITTER
# -------------------------------------------------------------
if section == "🥞 PDF Splitter":
    st.markdown("<div class='main-header'>🥞 PDF Splitter</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Split PDFs into custom ranges with instant downloads - inspired by I Love PDF.</div>", unsafe_allow_html=True)

    uploaded_pdf = st.file_uploader("Upload your GATE Question Bank PDF", type=["pdf"])

    if uploaded_pdf:
        # Load PDF metadata
        pdf_bytes = uploaded_pdf.read()
        reader = PdfReader(BytesIO(pdf_bytes))
        total_pages = len(reader.pages)
        
        st.success(f"Successfully loaded '{uploaded_pdf.name}' | Total Pages: {total_pages}")
        
        # Interactive Range Customizer
        st.subheader("Define Custom Splits")
        
        if "ranges" not in st.session_state:
            st.session_state.ranges = [{"start": 1, "end": min(5, total_pages), "name": "Split_Part_1"}]
            
        col1, col2 = st.columns([3, 1])
        
        with col2:
            if st.button("➕ Add Another Range"):
                st.session_state.ranges.append({
                    "start": 1,
                    "end": min(5, total_pages),
                    "name": f"Split_Part_{len(st.session_state.ranges) + 1}"
                })
            if st.button("🧹 Clear All Ranges") and len(st.session_state.ranges) > 0:
                st.session_state.ranges = [{"start": 1, "end": min(5, total_pages), "name": "Split_Part_1"}]
        
        # Render ranges inputs
        updated_ranges = []
        with col1:
            for idx, r in enumerate(st.session_state.ranges):
                with st.container():
                    st.markdown(f"**Range #{idx + 1}**")
                    c_name, c_start, c_end, c_btn = st.columns([3, 2, 2, 1])
                    
                    val_name = c_name.text_input("Output Filename", value=r["name"], key=f"name_{idx}")
                    val_start = c_start.number_input("Start Page", min_value=1, max_value=total_pages, value=min(r["start"], total_pages), key=f"start_{idx}")
                    val_end = c_end.number_input("End Page", min_value=1, max_value=total_pages, value=min(r["end"], total_pages), key=f"end_{idx}")
                    
                    delete_pressed = c_btn.button("🗑️", key=f"del_{idx}")
                    
                    if not delete_pressed:
                        updated_ranges.append({"start": val_start, "end": val_end, "name": val_name})
            
            st.session_state.ranges = updated_ranges

        if st.button("🚀 Process & Split PDF", type="primary"):
            if not st.session_state.ranges:
                st.warning("Please define at least one range.")
            else:
                progress_bar = st.progress(0)
                zip_buffer = BytesIO()
                
                # Check if we should package multiple PDFs into a ZIP or offer single download
                split_files = []
                
                for i, r in enumerate(st.session_state.ranges):
                    start_idx = r["start"] - 1
                    end_idx = r["end"]
                    out_name = r["name"].strip()
                    if not out_name.endswith(".pdf"):
                        out_name += ".pdf"
                        
                    if start_idx < 0 or end_idx > total_pages or start_idx >= end_idx:
                        st.error(f"Invalid range for '{r['name']}': Pages {r['start']} to {r['end']}. Ignoring.")
                        continue
                    
                    # Create split PDF
                    writer = PdfWriter()
                    for page_num in range(start_idx, end_idx):
                        writer.add_page(reader.pages[page_num])
                        
                    out_pdf_bytes = BytesIO()
                    writer.write(out_pdf_bytes)
                    split_files.append((out_name, out_pdf_bytes.getvalue()))
                    
                    progress_bar.progress((i + 1) / len(st.session_state.ranges))
                
                progress_bar.empty()
                st.success("Successfully split the PDF document!")
                
                if len(split_files) == 1:
                    # Single file download button
                    name, data = split_files[0]
                    st.download_button(
                        label=f"📥 Download {name}",
                        data=data,
                        file_name=name,
                        mime="application/pdf"
                    )
                elif len(split_files) > 1:
                    # Zip multiple files
                    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
                        for name, data in split_files:
                            zip_file.writestr(name, data)
                            
                    st.download_button(
                        label="📥 Download All Splits as ZIP",
                        data=zip_buffer.getvalue(),
                        file_name="split_pdfs.zip",
                        mime="application/zip"
                    )

# -------------------------------------------------------------
# SECTION 2: JSON IMPORTER
# -------------------------------------------------------------
elif section == "📥 JSON Importer":
    st.markdown("<div class='main-header'>📥 JSON Question Importer</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Upload structured questions in JSON format to seamlessly bulk upload into Supabase.</div>", unsafe_allow_html=True)

    # Supabase connection status check
    connected = test_supabase_connection()
    if not connected:
        st.error("⚠️ Supabase connection failed. Please check your `.env` config credentials.")
    else:
        st.success("🟢 Supabase database connected successfully!")

    uploaded_json = st.file_uploader("Upload your GATE questions JSON file", type=["json"])
    
    if uploaded_json:
        try:
            import_data = json.load(uploaded_json)
            
            # Simple validation & preview structure
            subject = import_data.get("subject", {})
            topics = import_data.get("topics", [])
            questions = import_data.get("questions", [])
            
            st.markdown("### Preview & Data Summary")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Subject Name", subject.get("subject_name", "N/A"))
            with col2:
                st.metric("Total Topics Found", len(topics))
            with col3:
                st.metric("Total Questions Found", len(questions))
                
            # Expandable preview of questions
            with st.expander("🔍 View First 3 Questions Preview"):
                for index, q in enumerate(questions[:3]):
                    st.markdown(f"**Q{index+1}:** {q.get('question_text')}")
                    st.json(q.get("options", []))
                    st.write(f"*Explanation:* {q.get('explanation')}")
                    st.divider()

            if st.button("🚀 Confirm & Run Import into Supabase", type="primary"):
                # Use dynamic importer logic here
                with st.spinner("Uploading and syncing database entities..."):
                    # Call GateImporter dynamically or custom runner
                    try:
                        from importer import GateImporter
                        importer = GateImporter(rollback_on_failure=True)
                        importer.run_import(import_data)
                        st.success("🎉 Import completed successfully! Database has been updated.")
                    except Exception as err:
                        st.error(f"Failed during import: {err}")
        except Exception as e:
            st.error(f"Error parsing JSON file: {e}")

# -------------------------------------------------------------
# SECTION 3: QUESTION DATABASE CRUD EDITOR
# -------------------------------------------------------------
elif section == "🔐 Question Database Editor (Protected)":
    st.markdown("<div class='main-header'>🔐 Question Database Editor</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Manage, add, modify, and delete questions, options, and explanations in the Supabase schema.</div>", unsafe_allow_html=True)

    # Password check
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "gateadmin8059")
    
    # Session state for auth
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
        
    if not st.session_state.admin_authenticated:
        password_input = st.text_input("Enter Admin Password to Unlock Section", type="password")
        if st.button("Unlock"):
            if password_input == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("❌ Incorrect Password!")
    else:
        # Logged in UI
        if st.sidebar.button("🔒 Lock Dashboard"):
            st.session_state.admin_authenticated = False
            st.rerun()
            
        # Connected Check
        connected = test_supabase_connection()
        if not connected:
            st.error("⚠️ Supabase connection offline. Editor is unavailable.")
        else:
            # Let's read subject list
            subjects = db_select("gate_subjects")
            subject_options = {s["name"]: s["id"] for s in subjects}
            
            # Select subject
            selected_subj_name = st.selectbox("Select Subject", list(subject_options.keys()))
            
            if selected_subj_name:
                subj_id = subject_options[selected_subj_name]
                
                # Fetch questions for this subject
                questions = db_select("gate_questions", {"subject_id": f"eq.{subj_id}"})
                
                tab_edit, tab_add = st.tabs(["✏️ Edit/Delete Questions", "➕ Add New Question"])
                
                # -------------------------------------------------------------
                # SUBTAB 1: EDIT / DELETE
                # -------------------------------------------------------------
                with tab_edit:
                    if not questions:
                        st.info("No questions found in database for this subject.")
                    else:
                        st.write(f"Total questions found: {len(questions)}")
                        
                        # Search question text
                        search_q = st.text_input("Search Question text")
                        filtered_q = questions
                        if search_q:
                            filtered_q = [q for q in questions if search_q.lower() in q["question_text"].lower()]
                            
                        # Select question to edit
                        q_choices = {f"{q['id']} - {q['question_text'][:80]}...": q for q in filtered_q}
                        selected_q_label = st.selectbox("Select Question to Edit", list(q_choices.keys()))
                        
                        if selected_q_label:
                            q_data = q_choices[selected_q_label]
                            q_id = q_data["id"]
                            
                            st.markdown("### Question Details")
                            
                            edit_text = st.text_area("Question Text", value=q_data.get("question_text", ""))
                            c1, c2, c3 = st.columns(3)
                            edit_type = c1.selectbox("Question Type", ["MCQ", "NAT", "MSQ"], index=["MCQ", "NAT", "MSQ"].index(q_data.get("question_type", "MCQ")))
                            edit_marks = c2.number_input("Marks", min_value=1, max_value=5, value=int(q_data.get("marks", 1)))
                            edit_difficulty = c3.selectbox("Difficulty", ["easy", "medium", "hard"], index=["easy", "medium", "hard"].index(q_data.get("difficulty", "medium")))
                            
                            edit_explanation = st.text_area("Explanation/Solution", value=q_data.get("explanation", ""))
                            
                            # Options edit
                            st.markdown("#### Options / Choice Config (For MCQs/MSQs)")
                            q_options = db_select("gate_options", {"question_id": f"eq.{q_id}"})
                            
                            updated_options_data = []
                            for idx, opt in enumerate(q_options):
                                st.markdown(f"**Option {opt.get('option_label', idx+1)}**")
                                oc1, oc2, oc3 = st.columns([1, 4, 1])
                                label_val = oc1.text_input(f"Label {idx+1}", value=opt.get("option_label", ""), key=f"opt_lbl_{opt['id']}")
                                text_val = oc2.text_input(f"Text {idx+1}", value=opt.get("option_text", ""), key=f"opt_txt_{opt['id']}")
                                correct_val = oc3.checkbox(f"Correct", value=opt.get("is_correct", False), key=f"opt_corr_{opt['id']}")
                                updated_options_data.append({
                                    "id": opt["id"],
                                    "option_label": label_val,
                                    "option_text": text_val,
                                    "is_correct": correct_val
                                })
                            
                            # Update Button Actions
                            sub_c1, sub_c2 = st.columns(2)
                            if sub_c1.button("💾 Save Changes", type="primary"):
                                # Update Question
                                q_fields = {
                                    "question_text": edit_text,
                                    "question_type": edit_type,
                                    "marks": edit_marks,
                                    "difficulty": edit_difficulty,
                                    "explanation": edit_explanation
                                }
                                q_ok = db_update("gate_questions", q_fields, {"id": f"eq.{q_id}"})
                                
                                # Update Options
                                opt_ok = True
                                for opt_info in updated_options_data:
                                    res_opt = db_update("gate_options", {
                                        "option_label": opt_info["option_label"],
                                        "option_text": opt_info["option_text"],
                                        "is_correct": opt_info["is_correct"]
                                    }, {"id": f"eq.{opt_info['id']}"})
                                    if not res_opt:
                                        opt_ok = False
                                        
                                if q_ok and opt_ok:
                                    st.success("Successfully updated question and options!")
                                    st.rerun()
                                else:
                                    st.error("Failed to update question metadata.")
                                    
                            if sub_c2.button("🗑️ Delete Question", type="secondary"):
                                # Cascading delete handles options and occurrences
                                # Let's perform deletions
                                db_delete("gate_options", {"question_id": f"eq.{q_id}"})
                                db_delete("gate_question_topics", {"question_id": f"eq.{q_id}"})
                                db_delete("gate_question_concepts", {"question_id": f"eq.{q_id}"})
                                db_delete("gate_question_tags", {"question_id": f"eq.{q_id}"})
                                db_delete("gate_question_occurrences", {"question_id": f"eq.{q_id}"})
                                db_delete("gate_question_prerequisites", {"question_id": f"eq.{q_id}"})
                                db_delete("gate_common_mistakes", {"question_id": f"eq.{q_id}"})
                                db_delete("gate_related_concepts", {"question_id": f"eq.{q_id}"})
                                
                                ok = db_delete("gate_questions", {"id": f"eq.{q_id}"})
                                if ok:
                                    st.success("Question deleted completely!")
                                    st.rerun()
                                else:
                                    st.error("Failed to delete question record.")
                                    
                # -------------------------------------------------------------
                # SUBTAB 2: ADD NEW
                # -------------------------------------------------------------
                with tab_add:
                    st.markdown("### Create New Question")
                    new_text = st.text_area("Question Text", key="new_q_text")
                    
                    nc1, nc2, nc3 = st.columns(3)
                    new_type = nc1.selectbox("Question Type", ["MCQ", "NAT", "MSQ"], key="new_q_type")
                    new_marks = nc2.number_input("Marks", min_value=1, max_value=5, value=1, key="new_q_marks")
                    new_difficulty = nc3.selectbox("Difficulty", ["easy", "medium", "hard"], key="new_q_diff")
                    
                    new_explanation = st.text_area("Explanation/Solution", key="new_q_expl")
                    
                    st.markdown("#### Configure Options (For MCQ/MSQ)")
                    num_opts = st.number_input("Number of Options", min_value=0, max_value=6, value=4)
                    
                    new_options_input = []
                    for k in range(int(num_opts)):
                        st.markdown(f"**New Option #{k+1}**")
                        noc1, noc2, noc3 = st.columns([1, 4, 1])
                        nl = noc1.text_input(f"Option Label", value=chr(65+k), key=f"new_opt_lbl_{k}")
                        nt = noc2.text_input(f"Option Text", key=f"new_opt_txt_{k}")
                        nc = noc3.checkbox(f"Is Correct Answer", key=f"new_opt_corr_{k}")
                        new_options_input.append({
                            "option_label": nl,
                            "option_text": nt,
                            "is_correct": nc
                        })
                        
                    if st.button("➕ Insert New Question Record", type="primary"):
                        if not new_text.strip():
                            st.warning("Please provide question text.")
                        else:
                            q_fields = {
                                "subject_id": subj_id,
                                "question_text": new_text,
                                "question_type": new_type,
                                "marks": new_marks,
                                "difficulty": new_difficulty,
                                "explanation": new_explanation
                            }
                            res = db_insert("gate_questions", q_fields)
                            if res:
                                q_new_id = res[0]["id"]
                                
                                # Insert options
                                opt_count = 0
                                for o in new_options_input:
                                    o["question_id"] = q_new_id
                                    db_insert("gate_options", o)
                                    opt_count += 1
                                    
                                st.success(f"Successfully created question ID {q_new_id} with {opt_count} options!")
                                st.rerun()
                            else:
                                st.error("Failed to insert new question record.")
