import os
from dotenv import load_dotenv
from supabase import create_client

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def get_subjects():
    """Retrieve all subjects sorted by name."""
    result = (
        supabase
        .table("subjects")
        .select("id, name, code, yt_links")
        .order("name")
        .execute()
    )
    return result.data

def update_yt_links(subject_id: str, yt_links: list):
    """Update the yt_links column for a specific subject ID."""
    result = (
        supabase
        .table("subjects")
        .update({"yt_links": yt_links})
        .eq("id", subject_id)
        .execute()
    )
    return result.data

def get_branches():
    """Retrieve all branches sorted by name."""
    result = supabase.table("branches").select("id, name").order("name").execute()
    return result.data

def get_years():
    """Retrieve all years sorted by name."""
    result = supabase.table("years").select("id, name").order("name").execute()
    return result.data

def create_branch(name: str):
    """Create a new branch if not already exists."""
    result = supabase.table("branches").insert({"name": name}).execute()
    return result.data[0] if result.data else None

def create_year(name: str):
    """Create a new year if not already exists."""
    result = supabase.table("years").insert({"name": name}).execute()
    return result.data[0] if result.data else None

def create_subject(name: str, code: str, pyq_drive_link: str = None, notes_drive_link: str = None, course_outcome_link: str = None):
    """Create a new subject."""
    data = {
        "name": name,
        "code": code,
        "pyq_drive_link": pyq_drive_link,
        "notes_drive_link": notes_drive_link,
        "course_outcome_link": course_outcome_link
    }
    result = supabase.table("subjects").insert(data).execute()
    return result.data[0] if result.data else None

def create_branch_subject_mapping(branch_id: str, subject_id: str, year_id: str, semester: int):
    """Create a mapping between branch, subject, year and semester."""
    data = {
        "branch_id": branch_id,
        "subject_id": subject_id,
        "year_id": year_id,
        "semester": semester
    }
    result = supabase.table("branch_subjects").insert(data).execute()
    return result.data[0] if result.data else None

def upload_pyq_json_data(subject_id: str, json_data: dict, progress_callback=None):
    """
    Parse and insert PYQ JSON data matching content_insertion.py logic.
    Accepts progress_callback(message: str) to report progress to caller.
    """
    topics = json_data.get("topics", [])
    questions = json_data.get("questions", [])

    if progress_callback:
        progress_callback(f"Inserting {len(topics)} topics...")

    topic_map = {} # name -> id
    for t in topics:
        res = supabase.table("topics").insert({
            "subject_id": subject_id,
            "name": t["topic_name"],
            "summary": t.get("summary")
        }).execute()
        if res.data:
            topic_map[t["topic_name"]] = res.data[0]["id"]

    if progress_callback:
        progress_callback(f"Inserting {len(questions)} questions...")

    for i, q in enumerate(questions):
        # Insert Question
        res_q = supabase.table("questions").insert({
            "question_text": q["question_text"],
            "difficulty": q.get("difficulty", "easy")
        }).execute()
        
        if not res_q.data:
            continue
        
        q_id = res_q.data[0]["id"]

        # Link Question to Topics
        for topic_name in q.get("topics", []):
            t_id = topic_map.get(topic_name)
            if t_id:
                supabase.table("question_topics").insert({
                    "question_id": q_id,
                    "topic_id": t_id
                }).execute()

        # PYQ Sources
        for src in q.get("pyq_sources", []):
            # Check if it already exists
            existing = supabase.table("pyq_sources").select("id").match({
                "year": src["year"],
                "exam_type": src["exam_type"],
                "season": src["season"],
                "question_number": src["question_number"],
                "subject_id": subject_id
            }).execute()

            if existing.data:
                pyq_id = existing.data[0]["id"]
            else:
                res_src = supabase.table("pyq_sources").insert({
                    **src,
                    "subject_id": subject_id
                }).execute()
                pyq_id = res_src.data[0]["id"] if res_src.data else None

            # Map Question <-> PYQ Source
            if pyq_id:
                supabase.table("question_pyq_map").insert({
                    "question_id": q_id,
                    "pyq_source_id": pyq_id
                }).execute()

        if progress_callback and (i + 1) % 5 == 0:
            progress_callback(f"Inserted {i + 1}/{len(questions)} questions...")

    if progress_callback:
        progress_callback("All data inserted successfully!")

