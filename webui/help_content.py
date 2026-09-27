"""Offline fallback help text (Firestore `info_guides/{key}` overrides these, like the desktop)."""

HELP = {
    "guide": {
        "title": "📚 FocusFox Workspace Guide",
        "image": "fox_happy.png",
        "text": (
            "✦ FocusFox Admin Workspace ✦\n"
            "This application acts as a secure back-office dashboard for managing course catalogs, lecture playlists, solution sets, and exam question databases.\n\n"
            "🏡 Navigation & Architecture:\n"
            "• Sidebar Navigation: Switch tabs instantly.\n"
            "• Theme: Switch Light/Dark from the ⋮ menu (top right) → Settings → Theme.\n"
            "• Database Connectivity: Cloud indicators (☁ Connected / ☁ Offline) reflect Supabase direct connection status.\n"
            "• Authentication: Powered by Google sign-in. Only allow-listed developer accounts can open the dashboard. Your session details are shown at the bottom of the sidebar.\n"
            "• Audit Logging: Your login, upload, import, and editor events are logged automatically in Firestore."
        ),
        "schema": (
            "Firestore Collections Schema:\n"
            "• users: { uid (str, PK), name (str), email (str), role (str), last_login (timestamp) }\n"
            "• activity_logs: { user_id (str), user_email (str), action (str), content_type (str), subject (str), timestamp (server_timestamp) }"
        ),
    },
    "yt": {
        "title": "🎥 College PYQ & YT Link Uploader Guide",
        "image": "lil_fox.png",
        "text": (
            "📺 YouTube Links Tab:\n"
            "• Purpose: Associating video resources with courses so students can view curated playlists.\n"
            "• Action: Select a subject. Edit the links (one full HTTP link per line). Click 'Save' to update the 'subjects' table in Supabase. You can filter subjects by whether they have video links.\n\n"
            "📚 Subject & Branch Tab:\n"
            "• This is to only be used if a subject does not already exist in the database and needs to be added, additionally if the corresponding branch and other meta data of the subject does not already exist, then the branch or other related data is to be added, else it is not required.\n"
            "• Purpose: Registering new subject units and mapping them to semesters, branches, and academic years.\n"
            "• Action: Input subject code & name, notes link, and syllabus details. Select semester (1-8), branch, and year. Click 'Create Subject' to register and map them.\n\n"
            "📥 JSON Importer Tab:\n"
            "• Purpose: Importing batch questions/topics list generated from PDF scrapers.\n"
            "• Go to the following links:\n"
            "  - https://drive.google.com/drive/folders/1Ugm0zGR4A1d-mZPjCemNmxV7IsPK7Skg?usp=drive_link\n"
            "  - kiitkatalog.gfgkiit.in\n"
            "  - http://10.2.0.26:4000/home (only works on kiit wifi)\n\n"
            "• Find the related subject's pyq there, download them along with the course handout (likely available in the drive) and put them in claude.ai with the prompt specified in the Firestore guide.\n\n"
            "• Action: Choose target subject and browse to your structured JSON and upload it. Progress is shown in the Import Log box."
        ),
        "schema": (
            "Supabase DB Tables Schema (College Unit Catalog):\n"
            "• subjects: { id (uuid, PK), name (text), code (text, unique), yt_links (text[]), pyq_drive_link (text), notes_drive_link (text), course_outcome_link (text) }\n"
            "• branches: { id (uuid, PK), name (text, unique) }\n"
            "• years: { id (uuid, PK), name (text, unique) }\n"
            "• branch_subjects: { id (uuid, PK), branch_id (FK), subject_id (FK), year_id (FK), semester (int) }\n"
            "• topics: { id (uuid, PK), subject_id (FK), name (text), summary (text) }\n"
            "• questions: { id (uuid, PK), question_text (text), difficulty (enum) }\n"
            "• question_topics: { id (uuid, PK), question_id (FK), topic_id (FK) }\n"
            "• pyq_sources: { id (uuid, PK), subject_id (FK), year (int), exam_type (enum), season (enum), question_number (text) }\n"
            "• question_pyq_map: { id (uuid, PK), question_id (FK), pyq_source_id (FK) }"
        ),
    },
    "gate": {
        "title": "🎓 GATE Admin Portal Guide",
        "image": "owl.png",
        "text": (
            "🗂 PDF Splitter Tab:\n"
            "• Purpose: Splitting large multi-chapter PDFs into specific topic modules to make them easily queryable.\n"
            "• Action: Upload a source PDF. Define ranges (e.g. 1-10, 11-20, according to chapter starting and ending point, including the chapter solution), name the files, and click split. The split files download as a ZIP.\n\n"
            "• Put them in claude.ai with the GATE PYQ extraction assistant prompt specified in the Firestore guide.\n\n"
            "📥 JSON Importer Tab:\n"
            "• Purpose: Seeding core GATE question banks into Supabase tables.\n"
            "• Action: Upload structured GATE JSON. The importer parses subjects, papers, options, and correctness tags, then syncs them."
        ),
        "schema": (
            "Supabase DB Tables Schema (GATE Core):\n"
            "• gate_subjects: { id, name (text), code (text, unique), display_order (int) }\n"
            "• gate_topics: { id, subject_id (FK), name (text), summary (text) }\n"
            "• gate_questions: { id, subject_id (FK), question_text (text), explanation (text), question_type (text), marks (int), difficulty (text) }\n"
            "• gate_options: { id, question_id (FK), option_label (text), option_text (text), is_correct (bool) }\n"
            "• gate_question_topics: { id, question_id (FK), topic_id (FK) }\n"
            "• gate_papers: { id, exam (text), year (int), set_number (int) }\n"
            "• gate_question_occurrences: { id, question_id (FK), paper_id (FK), question_number }"
        ),
    },
    "college_img": {
        "title": "🖼️ College Solution Image Uploader Guide",
        "image": "panda.png",
        "text": (
            "🎨 Interface Workflow:\n"
            "• Left Panel: Cascade dropdowns. Filter by Branch -> Sem -> Subject -> Year -> Exam -> Season -> Question. Selecting a question shows its body text in the preview box.\n\n"
            "⚡ Image Upload & CDN:\n"
            "• Right Panel: Click 'Choose Images' to select multiple step-by-step solution pages (in order). Thumbnails will appear in the grid.\n"
            "• Upload: Clicking 'Upload' pushes files directly to ImageKit CDN (images/<question_id>/1.png, 2.png …) and maps the CDN URLs into Supabase.\n"
            "• Note: Solution uploads replace existing images for the selected question."
        ),
        "schema": (
            "Supabase DB Tables Schema (College Image Mapping):\n"
            "• images: { id (uuid, PK), question_id (FK), image_url (text), order_index (int) }"
        ),
    },
    "gate_img": {
        "title": "📐 GATE Image Uploader Guide",
        "image": "lil_fox.png",
        "text": (
            "🎨 Interface Workflow:\n"
            "• Left Panel: Select Year -> Paper -> Subject -> Question.\n"
            "• Target Selection: Decide if the images belong to the main Question Body or a specific Option (A, B, C, D).\n\n"
            "⚡ Image Upload & CDN:\n"
            "• Right Panel: Select images and click 'Upload'. Files are sent to ImageKit CDN (saved under 'gate/questions/<id>' or 'gate/options/<id>').\n"
            "• Note: Question and option images are overwritten upon new uploads."
        ),
        "schema": (
            "Supabase DB Tables Schema (GATE Image Mapping):\n"
            "• gate_question_images: { id, question_id (FK), image_url (text), order_index (int) }\n"
            "• gate_option_images: { id, option_id (FK), image_url (text), order_index (int) }"
        ),
    },
    "gate_db": {
        "title": "📁 GATE DB Editor Guide (Protected)",
        "image": "raccoon.png",
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
        ),
    },
    "todo": {
        "title": "📝 Developer Tasks Guide",
        "image": "coffee.png",
        "text": (
            "✦ Developer Task Manager ✦\n"
            "Keep track of milestones, features, and fixes directly inside the workspace.\n\n"
            "⚙️ Features:\n"
            "• Add Task: Write tasks in the text field at the top and click 'Add Task' or press Enter.\n"
            "• Completed State: Tick the checkbox to mark the task completed. This applies a line-through styling.\n"
            "• Persistent State: Completed status and deletes are saved to Firestore immediately.\n"
            "• Multi-User isolation: Tasks are fetched and saved under the logged-in developer's profile (same tasks as the desktop app)."
        ),
        "schema": (
            "Firestore Document Mapping:\n"
            "• Collection: todos/{todo_id}\n"
            "• Fields: { user_id (str), text (str), completed (bool), created_at (timestamp) }"
        ),
    },
    "spotify": {
        "title": "🎵 Focus Music Player Guide",
        "image": "coffee.png",
        "text": (
            "Integrates Spotify focus music into your coding workspace.\n\n"
            "1. Play here: Plays the playlist in an embedded Spotify player inside the dashboard.\n"
            "2. Open App: Launches the Spotify Desktop application directly to the playlist.\n"
            "3. Open Web: Opens the playlist on open.spotify.com in a new tab.\n"
            "4. Custom Playlists: Paste your own Spotify playlist link and click 'Save'. It will sync with Firestore so it is saved to your account profile."
        ),
        "schema": "Spotify integration settings are mapped per-user in Firestore (spotify_settings/{uid}).",
    },
}
