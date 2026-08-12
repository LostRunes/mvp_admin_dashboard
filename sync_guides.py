import os
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore
SERVICE_ACCT_PATH = "firebase_service_account.json"
if not os.path.exists(SERVICE_ACCT_PATH):
    print("firebase_service_account.json not found!")
    exit(1)

cred = credentials.Certificate(SERVICE_ACCT_PATH)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

DETAILED_GUIDES = {
    "guide": {
        "image": "fox_happy.png",
        "title": "📚 FocusFox Workspace Guide",
        "text": (
            "✦ FocusFox Admin Workspace ✦\n"
            "This application acts as a secure back-office dashboard for managing course catalogs, lecture playlists, solution sets, and exam question databases.\n\n"
            "🏡 Navigation & Architecture:\n"
            "• Sidebar Navigation: Switch tabs instantly. The interface updates colors based on theme palettes.\n"
            "• Theme Toggle: Swap between Light/Dark mode. State defaults to Dark Mode on startup.\n"
            "• Database Connectivity: Cloud indicators (☁ Connected / ☁ Offline) reflect Supabase direct connection status.\n"
            "• Authentication: Powered by Google OAuth. Your developer session details are shown at the bottom of the sidebar.\n"
            "• Audit Logging: Your login, upload, import, and editor events are logged automatically in Firestore."
        ),
        "schema": (
            "Firestore Collections Schema:\n"
            "• users: { uid (str, PK), name (str), email (str), role (str), last_login (timestamp) }\n"
            "• activity_logs: { user_id (str), user_email (str), action (str), content_type (str), subject (str), timestamp (server_timestamp) }"
        )
    },
    "yt": {
        "image": "lil_fox.png",
        "title": "🎥 College PYQ & YT Link Uploader Guide",
        "text": (
            "📺 YouTube Links Tab:\n"
            "• Purpose: Associating video resources with courses so students can view curated playlists.\n"
            "• Action: Select a subject. Edit the links (one full HTTP link per line). Click 'Save' to update the 'subjects' table in Supabase. You can filter subjects by whether they have video links.\n\n"
            "📚 Subject & Branch Tab:\n"
            "• Purpose: Registering new subject units and mapping them to semesters, branches, and academic years.\n"
            "• Action: Input subject code & name, notes link, and syllabus details. Select semester (1-8), branch, and year. Click 'Create Subject' to register and map them.\n\n"
            "📥 JSON Importer Tab:\n"
            "• Purpose: Importing batch questions/topics list generated from PDF scrapers.\n"
            "• Action: Choose target subject and browse to your structured JSON. Progress is shown in the Import Log box."
        ),
        "schema": (
            "Supabase DB Tables Schema (College Unit Catalog):\n"
            "• subjects: { id (int, PK), name (text), code (text, unique), yt_links (text[]), pyq_drive_link (text), notes_drive_link (text), course_outcome_link (text) }\n"
            "• branches: { id (int, PK), name (text, unique) }\n"
            "• years: { id (int, PK), name (text, unique) }\n"
            "• branch_subjects: { id (int, PK), branch_id (int, FK), subject_id (int, FK), year_id (int, FK), semester (int) }\n"
            "• topics: { id (int, PK), subject_id (int, FK), name (text), summary (text) }\n"
            "• questions: { id (int, PK), question_text (text), difficulty (text) }\n"
            "• question_topics: { id (int, PK), question_id (int, FK), topic_id (int, FK) }\n"
            "• pyq_sources: { id (int, PK), subject_id (int, FK), exam (text), year (int), season (text) }\n"
            "• question_pyq_map: { id (int, PK), question_id (int, FK), pyq_source_id (int, FK) }"
        )
    },
    "gate": {
        "image": "owl.png",
        "title": "🎓 GATE Admin Portal Guide",
        "text": (
            "🗂 PDF Splitter Tab:\n"
            "• Purpose: Splitting large multi-chapter PDFs into specific topic modules to make them easily queryable.\n"
            "• Action: Select a source PDF. Define ranges (e.g. 1-10, 11-20), name the files, select destination directory, and click split. It runs offline instantly.\n\n"
            "📥 JSON Importer Tab:\n"
            "• Purpose: Seeding core GATE question banks into Supabase tables.\n"
            "• Action: Browse structured GATE JSON. The importer parses subjects, papers, options, and correctness tags, then syncs them."
        ),
        "schema": (
            "Supabase DB Tables Schema (GATE Core):\n"
            "• gate_subjects: { id (int, PK), name (text), code (text, unique), display_order (int) }\n"
            "• gate_topics: { id (int, PK), subject_id (int, FK), name (text), summary (text) }\n"
            "• gate_questions: { id (int, PK), subject_id (int, FK), question_text (text), explanation (text), question_type (text), marks (int), difficulty (text) }\n"
            "• gate_options: { id (int, PK), question_id (int, FK), option_label (text), option_text (text), is_correct (bool) }\n"
            "• gate_question_topics: { id (int, PK), question_id (int, FK), topic_id (int, FK) }\n"
            "• gate_papers: { id (int, PK), exam (text), year (int), set_number (int) }\n"
            "• gate_question_occurrences: { id (int, PK), question_id (int, FK), paper_id (int, FK), question_number (int) }"
        )
    },
    "college_img": {
        "image": "panda.png",
        "title": "🖼️ College Solution Image Uploader Guide",
        "text": (
            "🎨 Interface Workflow:\n"
            "• Left Panel: Cascade dropdowns. Filter by Branch -> Sem -> Subject -> Year -> Exam -> Season -> Question. Selecting a question shows its body text in the preview box.\n\n"
            "⚡ Image Upload & CDN:\n"
            "• Right Panel: Click 'Choose Images' to select multiple step-by-step solution pages. Thumbnails will appear in the grid.\n"
            "• Upload: Clicking 'Upload' pushes files directly to ImageKit CDN and maps the CDN URLs into Supabase.\n"
            "• Note: Solution uploads replace existing images for the selected question."
        ),
        "schema": (
            "Supabase DB Tables Schema (College Image Mapping):\n"
            "• question_images: { id (int, PK), question_id (int, FK), image_url (text), display_order (int) }"
        )
    },
    "gate_img": {
        "image": "lil_fox.png",
        "title": "📐 GATE Image Uploader Guide",
        "text": (
            "🎨 Interface Workflow:\n"
            "• Left Panel: Select Year -> Paper -> Subject -> Question.\n"
            "• Target Selection: Decide if the image belongs to the main Question Body or specific Options (A, B, C, D).\n\n"
            "⚡ Image Upload & CDN:\n"
            "• Right Panel: Select images and click 'Upload'. Files are sent to ImageKit CDN (saved under 'gate/questions/<id>' or 'gate/options/<id>').\n"
            "• Note: Solutions and option images are overwritten upon new uploads."
        ),
        "schema": (
            "Supabase DB Tables Schema (GATE Image Mapping):\n"
            "• gate_questions (question_image_url field updated)\n"
            "• gate_options (option_image_url field updated)"
        )
    },
    "gate_db": {
        "image": "raccoon.png",
        "title": "📁 GATE DB Editor Guide (Protected)",
        "text": (
            "🔒 Protection:\n"
            "• Password prompt ensures only authorized developers modify database records.\n\n"
            "✏️ Editor Features:\n"
            "• Select subject and search by keywords to load question sets.\n"
            "• Click a question row to edit Question Text, Difficulty, Marks, and Explanation on the right panel.\n"
            "• Options Panel: Add options (+), delete options (trash), edit labels (A, B, C), edit text, and toggle correctness (True/False).\n"
            "• Click 'Save Changes' to update Supabase, or 'Delete Question' to remove the question and all associated option records."
        ),
        "schema": (
            "Supabase DB Tables Schema:\n"
            "• CRUD operations target gate_questions and gate_options direct structures."
        )
    },
    "todo": {
        "image": "coffee.png",
        "title": "📝 Developer Tasks Guide",
        "text": (
            "✦ Developer Task Manager ✦\n"
            "Keep track of milestones, features, and fixes directly inside the workspace.\n\n"
            "⚙️ Features:\n"
            "• Add Task: Write tasks in the text field at the top and click 'Add Task' or press Enter.\n"
            "• Completed State: Click the check button (⬜ -> ✔️) to mark the task completed. This applies a line-through styling.\n"
            "• Persistent State: Completed status and deletes are automatically updated in real-time in the background.\n"
            "• Multi-User isolation: Tasks are fetched and saved under the logged-in developer's profile."
        ),
        "schema": (
            "Firestore Document Mapping:\n"
            "• Doc: users/{uid}/todos/{todo_id}\n"
            "• Fields: { text (str), completed (bool), created_at (timestamp) }"
        )
    }
}

print("Syncing guides to Firestore collection 'info_guides'...")
for key, guide in DETAILED_GUIDES.items():
    db.collection("info_guides").document(key).set(guide)
    # Print safe ascii text to avoid encoding crash
    safe_title = guide['title'].encode('ascii', 'ignore').decode()
    print(f"  Synced: {key} -> {safe_title}")
print("Sync complete!")
