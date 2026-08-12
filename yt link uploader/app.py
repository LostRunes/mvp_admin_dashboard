from nicegui import ui
import re
import json
from supabase_service import (
    get_subjects, 
    update_yt_links, 
    get_branches, 
    get_years, 
    create_branch, 
    create_year, 
    create_subject, 
    create_branch_subject_mapping, 
    upload_pyq_json_data
)

# Custom CSS styling for premium feel
ui.add_head_html("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
    body {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #020617 100%);
        background-attachment: fixed;
        color: #f8fafc;
    }
    .glass-card {
        background: rgba(30, 41, 59, 0.45);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.3s ease;
    }
    .glass-card:hover {
        border-color: rgba(255, 255, 255, 0.15);
    }
    .input-field input {
        color: #f8fafc !important;
    }
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.5);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(99, 102, 241, 0.3);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(99, 102, 241, 0.5);
    }
</style>
""")

# Load initial data
try:
    subjects = get_subjects()
    branches = get_branches()
    years = get_years()
except Exception as e:
    subjects = []
    branches = []
    years = []
    print(f"Error loading initial database values: {e}")

subject_map = {
    f"{s['name']} ({s['code']})": s
    for s in subjects
}

branch_map = {b['name']: b for b in branches}
year_map = {y['name']: y for y in years}

# Application State
state = {
    "selected_subject": None,
    "current_links": [],
    "new_link": "",
    "filter": "All",  # "All", "With Links", "Without Links"
    
    # Subject Tab State
    "new_branch_name": "",
    "new_year_name": "",
    "new_subj_name": "",
    "new_subj_code": "",
    "new_subj_pyq_link": "",
    "new_subj_notes_link": "",
    "new_subj_co_link": "",
    "selected_branch": None,
    "selected_year": None,
    "selected_semester": 1,

    # Upload Tab State
    "upload_selected_subject": None,
    "upload_log": []
}

# Helpers
def is_valid_youtube_link(url: str) -> bool:
    pattern = r'^(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+$'
    return bool(re.match(pattern, url.strip()))

def get_filtered_options():
    options = []
    for s in subjects:
        has_links = bool(s.get("yt_links") and len(s["yt_links"]) > 0)
        opt_label = f"{s['name']} ({s['code']})"
        if state["filter"] == "All":
            options.append(opt_label)
        elif state["filter"] == "With Links" and has_links:
            options.append(opt_label)
        elif state["filter"] == "Without Links" and not has_links:
            options.append(opt_label)
    return options

def refresh_subjects_data():
    global subjects, subject_map
    try:
        subjects = get_subjects()
        subject_map = {f"{s['name']} ({s['code']})": s for s in subjects}
        subject_select.set_options(get_filtered_options())
        upload_subject_select.set_options([f"{s['name']} ({s['code']})" for s in subjects])
        ui.notify("Subjects list updated!", color="info")
    except Exception as e:
        ui.notify(f"Failed to refresh subjects: {e}", color="negative")

def refresh_branches_data():
    global branches, branch_map
    try:
        branches = get_branches()
        branch_map = {b['name']: b for b in branches}
        branch_select.set_options([b['name'] for b in branches])
        ui.notify("Branches list updated!", color="info")
    except Exception as e:
        ui.notify(f"Failed to refresh branches: {e}", color="negative")

def refresh_years_data():
    global years, year_map
    try:
        years = get_years()
        year_map = {y['name']: y for y in years}
        year_select.set_options([y['name'] for y in years])
        ui.notify("Years list updated!", color="info")
    except Exception as e:
        ui.notify(f"Failed to refresh years: {e}", color="negative")

# --- Event Handlers (Tab 1: YouTube Manager) ---
def on_subject_change(e):
    if not e.value:
        state["selected_subject"] = None
        state["current_links"] = []
    else:
        subj = subject_map[e.value]
        state["selected_subject"] = subj
        state["current_links"] = list(subj.get("yt_links") or [])
    
    links_list_container.refresh()
    details_container.refresh()

def on_filter_change(e):
    state["filter"] = e.value
    filtered = get_filtered_options()
    subject_select.set_options(filtered)
    if subject_select.value and subject_select.value not in filtered:
        subject_select.set_value(None)
    ui.notify(f"Filtered subjects: {state['filter']}", color="info")

def add_link():
    url = new_link_input.value or ""
    if not url.strip():
        ui.notify("Please enter a link", color="warning", icon="warning")
        return
    if not is_valid_youtube_link(url):
        ui.notify("Warning: This does not look like a standard YouTube URL", color="amber", icon="report_problem")
    
    state["current_links"].append(url.strip())
    new_link_input.set_value("")
    links_list_container.refresh()
    ui.notify("Link added (unsaved)", color="info", icon="playlist_add")

def delete_link(index: int):
    state["current_links"].pop(index)
    links_list_container.refresh()
    ui.notify("Link removed (unsaved)", color="orange", icon="delete")

def move_link_up(index: int):
    if index > 0:
        state["current_links"][index], state["current_links"][index - 1] = state["current_links"][index - 1], state["current_links"][index]
        links_list_container.refresh()

def move_link_down(index: int):
    if index < len(state["current_links"]) - 1:
        state["current_links"][index], state["current_links"][index + 1] = state["current_links"][index + 1], state["current_links"][index]
        links_list_container.refresh()

def update_link_val(index: int, value: str):
    state["current_links"][index] = value.strip()

async def save_links():
    if not state["selected_subject"]:
        ui.notify("Select a subject first", color="warning", icon="error")
        return
    
    subj = state["selected_subject"]
    links = [lnk for lnk in state["current_links"] if lnk.strip()]
    
    save_btn.props('loading')
    try:
        update_yt_links(subj["id"], links)
        subj["yt_links"] = list(links)
        state["current_links"] = list(links)
        ui.notify("YouTube links updated successfully!", color="positive", icon="check_circle")
    except Exception as e:
        ui.notify(f"Failed to save: {str(e)}", color="negative", icon="error")
    finally:
        save_btn.props(remove='loading')
        links_list_container.refresh()

def revert_changes():
    if not state["selected_subject"]:
        return
    state["current_links"] = list(state["selected_subject"].get("yt_links") or [])
    links_list_container.refresh()
    ui.notify("Reverted all unsaved changes", color="info", icon="undo")

# --- Event Handlers (Tab 2: Subject & Mappings) ---
def add_new_branch():
    name = state["new_branch_name"].strip()
    if not name:
        ui.notify("Branch name cannot be empty", color="warning")
        return
    try:
        create_branch(name)
        state["new_branch_name"] = ""
        new_branch_input.set_value("")
        refresh_branches_data()
        ui.notify(f"Branch '{name}' created successfully!", color="positive")
    except Exception as e:
        ui.notify(f"Failed to create branch: {e}", color="negative")

def add_new_year():
    name = state["new_year_name"].strip()
    if not name:
        ui.notify("Year name cannot be empty", color="warning")
        return
    try:
        create_year(name)
        state["new_year_name"] = ""
        new_year_input.set_value("")
        refresh_years_data()
        ui.notify(f"Year '{name}' created successfully!", color="positive")
    except Exception as e:
        ui.notify(f"Failed to create year: {e}", color="negative")

def add_subject_with_mapping():
    s_name = state["new_subj_name"].strip()
    s_code = state["new_subj_code"].strip()
    
    if not s_name or not s_code:
        ui.notify("Subject name and code are required", color="warning")
        return
        
    b_name = state["selected_branch"]
    y_name = state["selected_year"]
    sem = state["selected_semester"]
    
    if not b_name or not y_name:
        ui.notify("Please select Branch and Year for mapping", color="warning")
        return
        
    try:
        # Create Subject (Supabase automatically generates a unique UUID for this row)
        subj = create_subject(
            name=s_name,
            code=s_code,
            pyq_drive_link=state["new_subj_pyq_link"].strip() or None,
            notes_drive_link=state["new_subj_notes_link"].strip() or None,
            course_outcome_link=state["new_subj_co_link"].strip() or None
        )
        if not subj:
            ui.notify("Failed to create subject", color="negative")
            return
            
        # Get IDs
        branch_id = branch_map[b_name]["id"]
        year_id = year_map[y_name]["id"]
        
        # Map branch, subject, year, semester
        create_branch_subject_mapping(branch_id, subj["id"], year_id, sem)
        
        # Clear fields
        state["new_subj_name"] = ""
        state["new_subj_code"] = ""
        state["new_subj_pyq_link"] = ""
        state["new_subj_notes_link"] = ""
        state["new_subj_co_link"] = ""
        
        subj_name_input.set_value("")
        subj_code_input.set_value("")
        subj_pyq_input.set_value("")
        subj_notes_input.set_value("")
        subj_co_input.set_value("")
        
        refresh_subjects_data()
        ui.notify(f"Subject '{s_name}' created (UUID: {subj['id']}) and mapped successfully!", color="positive")
    except Exception as e:
        ui.notify(f"Error creating subject/mapping: {e}", color="negative")

# --- Event Handlers (Tab 3: Upload PYQ JSON) ---
def on_upload_subject_change(e):
    if not e.value:
        state["upload_selected_subject"] = None
    else:
        state["upload_selected_subject"] = subject_map[e.value]
    upload_details_container.refresh()

def log_progress(msg: str):
    state["upload_log"].append(msg)
    log_area.refresh()

async def handle_json_upload(e):
    if not state["upload_selected_subject"]:
        ui.notify("Please select a target subject first!", color="warning")
        return
        
    subj = state["upload_selected_subject"]
    state["upload_log"] = []
    log_progress(f"Starting upload for subject: {subj['name']} (ID: {subj['id']})")
    
    try:
        json_data = json.loads(e.content.read().decode('utf-8'))
        log_progress("Parsed JSON file successfully.")
        
        # Run upload logic
        upload_pyq_json_data(subj["id"], json_data, progress_callback=log_progress)
        ui.notify("JSON data uploaded and processed successfully!", color="positive")
    except Exception as ex:
        log_progress(f"ERROR: {str(ex)}")
        ui.notify(f"Upload failed: {ex}", color="negative")

# --- UI Layout ---

# Title header
with ui.row().classes('w-full justify-between items-center q-pa-md bg-transparent text-white'):
    with ui.row().classes('items-center gap-4'):
        ui.icon('dashboard', size='lg').classes('text-indigo-400')
        with ui.column().classes('gap-0'):
            ui.label('College PYQ & Resource Dashboard').classes('text-2xl font-extrabold tracking-tight')
            ui.label('Manage subjects, branches, mappings, and upload question bank JSONs').classes('text-xs text-slate-400')

# Main tab system (Three separate tabs)
with ui.tabs().classes('w-full text-indigo-200').props('active-color="white" indicator-color="indigo-500" dark') as tabs:
    tab_yt = ui.tab('YouTube Links', icon='video_library')
    tab_subj = ui.tab('Manage Subjects & Mappings', icon='settings')
    tab_pyq = ui.tab('Upload PYQ JSON', icon='cloud_upload')

with ui.tab_panels(tabs, value=tab_yt).classes('w-full bg-transparent text-white'):
    # ================= TAB 1: YOUTUBE MANAGER =================
    with ui.tab_panel(tab_yt):
        with ui.column().classes('w-full max-w-4xl mx-auto gap-6'):
            # Card 1: Selection and Filtering
            with ui.card().classes('glass-card w-full p-6 text-white'):
                ui.label('Subject Filter').classes('text-sm font-semibold mb-2 text-indigo-300')
                filter_toggle = ui.toggle(
                    ['All', 'With Links', 'Without Links'],
                    value=state["filter"],
                    on_change=on_filter_change
                ).classes('mb-4').props('dark color="indigo-400"')
                
                ui.label('Select Subject').classes('text-sm font-semibold mb-2 text-indigo-300')
                subject_select = ui.select(
                    options=get_filtered_options(),
                    label='Choose a subject...',
                    on_change=on_subject_change
                ).classes('w-full').props('outlined dark label-color="indigo-300" color="indigo-400"')

            # Card 2: Subject Details & Actions
            @ui.refreshable
            def details_container():
                subj = state["selected_subject"]
                if not subj:
                    return
                
                with ui.card().classes('glass-card w-full p-6 text-white'):
                    with ui.row().classes('w-full justify-between items-start'):
                        with ui.column().classes('gap-1'):
                            ui.label(subj['name']).classes('text-xl font-bold')
                            ui.label(f"Code: {subj['code']}").classes('text-sm text-slate-400')
                        
                    # Add Link Form
                    ui.separator().classes('my-4 opacity-10')
                    ui.label('Add YouTube Link').classes('text-sm font-semibold text-indigo-300 mb-1')
                    with ui.row().classes('w-full items-center gap-3'):
                        global new_link_input
                        new_link_input = ui.input(
                            placeholder='https://youtube.com/... or https://youtu.be/...'
                        ).classes('grow input-field').props('outlined dark color="indigo-400"')
                        
                        ui.button('Add Link', icon='add', on_click=add_link).classes('bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-4 py-2 rounded-lg').props('unelevated')

            details_container()

            # Card 3: Link List
            @ui.refreshable
            def links_list_container():
                subj = state["selected_subject"]
                if not subj:
                    with ui.card().classes('glass-card w-full p-12 text-center text-slate-400 flex flex-col items-center justify-center gap-2'):
                        ui.icon('smart_display', size='xl').classes('text-slate-600')
                        ui.label('Select a subject above to manage its YouTube links.').classes('text-sm font-medium')
                    return
                
                links = state["current_links"]
                
                with ui.card().classes('glass-card w-full p-6 text-white'):
                    with ui.row().classes('w-full justify-between items-center mb-4'):
                        ui.label(f'YouTube Links ({len(links)})').classes('text-lg font-semibold text-indigo-300')
                        
                        if links:
                            with ui.row().classes('gap-2'):
                                ui.button('Revert Changes', icon='undo', color='amber', on_click=revert_changes).props('outline dark')
                                global save_btn
                                save_btn = ui.button('Save Changes', icon='save', on_click=save_links).classes('bg-emerald-600 hover:bg-emerald-700 text-white').props('unelevated')
                    
                    if not links:
                        ui.label('No YouTube links added yet. Paste a link above to add.').classes('text-slate-400 italic text-sm my-4')
                        return
                    
                    # List items
                    with ui.column().classes('w-full gap-3 mt-2'):
                        for i, link in enumerate(links):
                            with ui.row().classes('w-full items-center gap-3 p-3 bg-slate-900/40 border border-slate-700/30 rounded-lg hover:border-slate-600/50 transition-all'):
                                ui.badge(str(i + 1), color='slate-800').classes('text-slate-300 font-bold px-2 py-1.5 rounded')
                                
                                ui.input(
                                    value=link,
                                    on_change=lambda e, idx=i: update_link_val(idx, e.value)
                                ).classes('grow input-field text-sm').props('outlined dark dense color="indigo-400"')
                                
                                with ui.row().classes('items-center gap-1'):
                                    ui.button(
                                        icon='open_in_new', 
                                        on_click=lambda l=link: ui.open(l, new_tab=True)
                                    ).props('flat round dense size="sm"').classes('text-indigo-400 hover:text-indigo-300')
                                    
                                    ui.button(
                                        icon='arrow_upward', 
                                        on_click=lambda idx=i: move_link_up(idx)
                                    ).props('flat round dense size="sm"').classes('text-slate-400 hover:text-white').set_visibility(i > 0)
                                    
                                    ui.button(
                                        icon='arrow_downward', 
                                        on_click=lambda idx=i: move_link_down(idx)
                                    ).props('flat round dense size="sm"').classes('text-slate-400 hover:text-white').set_visibility(i < len(links) - 1)
                                    
                                    ui.button(
                                        icon='delete', 
                                        color='rose', 
                                        on_click=lambda idx=i: delete_link(idx)
                                    ).props('flat round dense size="sm"').classes('text-rose-400 hover:text-rose-300')

            links_list_container()

    # ================= TAB 2: MANAGE SUBJECTS & MAPPINGS =================
    with ui.tab_panel(tab_subj):
        with ui.row().classes('w-full items-start gap-6'):
            # Left Sub-Column: Add Branch / Year
            with ui.column().classes('col-12 col-md-5 gap-6'):
                with ui.card().classes('glass-card w-full p-6 text-white'):
                    ui.label('Create New Branch or Year').classes('text-lg font-bold text-indigo-300 mb-2')
                    
                    with ui.row().classes('w-full items-center gap-3 mb-4'):
                        global new_branch_input
                        new_branch_input = ui.input(
                            label='Branch Name (e.g., Computer Science)',
                            on_change=lambda e: state.update({"new_branch_name": e.value})
                        ).classes('grow input-field').props('outlined dark color="indigo-400"')
                        ui.button('Add Branch', icon='add', on_click=add_new_branch).classes('bg-indigo-600 text-white').props('unelevated')
                        
                    with ui.row().classes('w-full items-center gap-3'):
                        global new_year_input
                        new_year_input = ui.input(
                            label='Academic Year (e.g., 3rd Year)',
                            on_change=lambda e: state.update({"new_year_name": e.value})
                        ).classes('grow input-field').props('outlined dark color="indigo-400"')
                        ui.button('Add Year', icon='add', on_click=add_new_year).classes('bg-indigo-600 text-white').props('unelevated')

            # Right Sub-Column: Subject Creation & Mappings Form
            with ui.column().classes('col-12 col-md-6 gap-6'):
                with ui.card().classes('glass-card w-full p-6 text-white'):
                    ui.label('Add Subject & Mappings').classes('text-lg font-bold text-indigo-300 mb-4')
                    
                    with ui.column().classes('w-full gap-4'):
                        global subj_name_input, subj_code_input, subj_pyq_input, subj_notes_input, subj_co_input
                        subj_name_input = ui.input(
                            label='Subject Name',
                            on_change=lambda e: state.update({"new_subj_name": e.value})
                        ).classes('w-full input-field').props('outlined dark color="indigo-400"')
                        
                        subj_code_input = ui.input(
                            label='Subject Code (Unique)',
                            on_change=lambda e: state.update({"new_subj_code": e.value})
                        ).classes('w-full input-field').props('outlined dark color="indigo-400"')
                        
                        subj_pyq_input = ui.input(
                            label='PYQ Drive Link (Optional)',
                            on_change=lambda e: state.update({"new_subj_pyq_link": e.value})
                        ).classes('w-full input-field').props('outlined dark color="indigo-400"')
                        
                        subj_notes_input = ui.input(
                            label='Notes Drive Link (Optional)',
                            on_change=lambda e: state.update({"new_subj_notes_link": e.value})
                        ).classes('w-full input-field').props('outlined dark color="indigo-400"')
                        
                        subj_co_input = ui.input(
                            label='Course Outcome Link (Optional)',
                            on_change=lambda e: state.update({"new_subj_co_link": e.value})
                        ).classes('w-full input-field').props('outlined dark color="indigo-400"')
                        
                        # Mapping section
                        ui.separator().classes('my-2 opacity-10')
                        ui.label('Branch & Year Mappings').classes('text-sm font-semibold text-indigo-300')
                        
                        with ui.row().classes('w-full gap-3'):
                            global branch_select
                            branch_select = ui.select(
                                options=[b['name'] for b in branches],
                                label='Branch',
                                on_change=lambda e: state.update({"selected_branch": e.value})
                            ).classes('grow').props('outlined dark color="indigo-400"')
                            
                            global year_select
                            year_select = ui.select(
                                options=[y['name'] for y in years],
                                label='Year',
                                on_change=lambda e: state.update({"selected_year": e.value})
                            ).classes('grow').props('outlined dark color="indigo-400"')
                            
                            ui.select(
                                options=[1, 2, 3, 4, 5, 6, 7, 8],
                                value=1,
                                label='Semester',
                                on_change=lambda e: state.update({"selected_semester": e.value})
                            ).classes('w-24').props('outlined dark color="indigo-400"')
                        
                        ui.button('Create Subject & Add Mappings', icon='save', on_click=add_subject_with_mapping).classes('w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3 rounded-lg').props('unelevated')

    # ================= TAB 3: UPLOAD PYQ JSON =================
    with ui.tab_panel(tab_pyq):
        with ui.column().classes('w-full max-w-4xl mx-auto gap-6'):
            with ui.card().classes('glass-card w-full p-6 text-white'):
                ui.label('Upload PYQ JSON').classes('text-xl font-bold text-indigo-300 mb-4')
                
                ui.label('Select Subject for Upload').classes('text-sm font-semibold text-slate-300 mb-1')
                global upload_subject_select
                upload_subject_select = ui.select(
                    options=[f"{s['name']} ({s['code']})" for s in subjects],
                    label='Choose subject...',
                    on_change=on_upload_subject_change
                ).classes('w-full mb-4').props('outlined dark color="indigo-400"')
                
                # Selected Subject details view
                @ui.refreshable
                def upload_details_container():
                    subj = state["upload_selected_subject"]
                    if not subj:
                        ui.label('No subject selected. Choose one to enable file uploader.').classes('text-slate-400 italic text-sm mb-4')
                        return
                    with ui.column().classes('w-full bg-slate-900/50 p-4 rounded-lg border border-slate-700/30 mb-4 gap-2'):
                        ui.label(f"Target Subject: {subj['name']}").classes('font-bold text-indigo-200')
                        ui.label(f"Subject Code: {subj['code']}").classes('text-xs text-slate-400')
                        ui.label(f"Subject UUID: {subj['id']}").classes('text-xs text-slate-400 font-mono')
                        
                        # File Upload Widget
                        ui.separator().classes('my-2 opacity-10')
                        ui.upload(
                            label='Drag & drop or click to upload JSON',
                            on_upload=handle_json_upload,
                            auto_upload=True
                        ).classes('w-full').props('dark flat color="indigo-400"')
                
                upload_details_container()
                
                # Log/Output area
                ui.separator().classes('my-4 opacity-10')
                ui.label('Progress Logs').classes('text-sm font-semibold text-indigo-300 mb-1')
                
                @ui.refreshable
                def log_area():
                    with ui.column().classes('w-full h-48 bg-slate-950/70 border border-slate-800 rounded-lg p-3 overflow-y-auto font-mono text-xs text-emerald-400 gap-1'):
                        if not state["upload_log"]:
                            ui.label('Logs will appear here once you select a subject and upload a file...').classes('text-slate-500 italic')
                        else:
                            for line in state["upload_log"]:
                                ui.label(line)
                
                log_area()

# Start application
ui.run(title='College PYQ & Resource Dashboard', port=8082, reload=False)
