from supabase import create_client
import config

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def get_branches():
    """Fetches all branches ordered by name."""
    result = supabase.table("branches").select("*").order("name").execute()
    return result.data

def get_semesters_by_branch(branch_id):
    """Fetches all distinct semesters linked to a branch."""
    result = supabase.table("branch_subjects")\
        .select("semester")\
        .eq("branch_id", branch_id)\
        .execute()
    
    semesters = sorted(list(set(row["semester"] for row in result.data if row.get("semester") is not None)))
    return semesters

def get_subjects_by_branch_and_semester(branch_id, semester):
    """Fetches all subjects linked to a branch and semester via branch_subjects table."""
    result = supabase.table("branch_subjects")\
        .select("subject_id, subjects(id, name, code)")\
        .eq("branch_id", branch_id)\
        .eq("semester", semester)\
        .execute()
    
    subjects = []
    seen_ids = set()
    for row in result.data:
        sub = row.get("subjects")
        if sub and sub["id"] not in seen_ids:
            seen_ids.add(sub["id"])
            subjects.append(sub)
            
    # Sort subjects by name
    subjects.sort(key=lambda x: x["name"].lower() if x.get("name") else "")
    return subjects


def get_years_by_subject(subject_id):
    """Fetches all distinct years available in pyq_sources for a subject."""
    result = supabase.table("pyq_sources")\
        .select("year")\
        .eq("subject_id", subject_id)\
        .execute()
    
    years = sorted(list(set(row["year"] for row in result.data if row.get("year") is not None)), reverse=True)
    return years

def get_exam_types_by_subject_and_year(subject_id, year):
    """Fetches all distinct exam types available in pyq_sources for a subject and year."""
    result = supabase.table("pyq_sources")\
        .select("exam_type")\
        .eq("subject_id", subject_id)\
        .eq("year", year)\
        .execute()
    
    exam_types = sorted(list(set(row["exam_type"] for row in result.data if row.get("exam_type") is not None)))
    return exam_types

def get_seasons_by_subject_year_and_exam_type(subject_id, year, exam_type):
    """Fetches all distinct seasons available in pyq_sources."""
    result = supabase.table("pyq_sources")\
        .select("season")\
        .eq("subject_id", subject_id)\
        .eq("year", year)\
        .eq("exam_type", exam_type)\
        .execute()
    
    seasons = sorted(list(set(row["season"] for row in result.data if row.get("season") is not None)))
    return seasons

def get_pyq_questions(subject_id, year, exam_type, season):
    """Fetches all pyq_sources questions matching the filters."""
    result = supabase.table("pyq_sources")\
        .select("id, question_number")\
        .eq("subject_id", subject_id)\
        .eq("year", year)\
        .eq("exam_type", exam_type)\
        .eq("season", season)\
        .execute()
    
    # Sort naturally if possible, or simple sorting
    questions = result.data
    try:
        # Simple attempt at natural sort: e.g. Q1a -> Q1, a
        def sort_key(q):
            num = q["question_number"]
            # Extract digits and trailing text
            digits = "".join(c for c in num if c.isdigit())
            alpha = "".join(c for c in num if not c.isdigit())
            return (int(digits) if digits else 999, alpha)
        questions.sort(key=sort_key)
    except Exception:
        questions.sort(key=lambda x: x["question_number"])
        
    return questions

def get_question_details(pyq_source_id):
    """Fetches the linked question text and actual question_id from question_pyq_map."""
    result = supabase.table("question_pyq_map")\
        .select("question_id, questions(question_text)")\
        .eq("pyq_source_id", pyq_source_id)\
        .execute()
    
    if result.data:
        row = result.data[0]
        q_data = row.get("questions")
        return {
            "question_id": row["question_id"],
            "question_text": q_data["question_text"] if q_data else "No text description."
        }
    return None

def get_existing_images(question_id):
    """Fetches all existing images for a question_id ordered by order_index."""
    result = supabase.table("images")\
        .select("*")\
        .eq("question_id", question_id)\
        .order("order_index")\
        .execute()
    return result.data

def delete_existing_images(question_id):
    """Deletes all existing images for a question_id."""
    return supabase.table("images").delete().eq("question_id", question_id).execute()

def insert_image_record(question_id, image_url, order_index):
    """Inserts a new image record into the images table."""
    return supabase.table("images").insert({
        "question_id": question_id,
        "image_url": image_url,
        "order_index": order_index
    }).execute()
