from supabase import create_client
import config
import re

supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def get_subjects():
    """Fetches all subjects from gate_subjects ordered by name."""
    result = supabase.table("gate_subjects").select("*").execute()
    subjects = result.data
    subjects.sort(key=lambda x: x.get("name") or "")
    return subjects

def get_years():
    """Fetches all distinct years from gate_papers ordered descending."""
    result = supabase.table("gate_papers").select("year").execute()
    years = sorted(list(set(row["year"] for row in result.data if row.get("year") is not None)), reverse=True)
    return years

def get_papers_by_year(year):
    """Fetches all papers for a given year."""
    result = supabase.table("gate_papers").select("*").eq("year", year).execute()
    papers = result.data
    # Sort by exam and then set_number
    papers.sort(key=lambda x: (x.get("exam") or "", x.get("set_number") or 0))
    return papers

def get_questions_by_paper(paper_id):
    """Fetches questions and occurrences for a paper, sorted naturally by question number."""
    result = supabase.table("gate_question_occurrences")\
        .select("question_id, question_number, gate_questions(id, question_text, explanation, subject_id)")\
        .eq("paper_id", paper_id)\
        .execute()
    
    questions = []
    for row in result.data:
        gq = row.get("gate_questions")
        if gq:
            questions.append({
                "question_id": row["question_id"],
                "question_number": row["question_number"],
                "question_text": gq.get("question_text") or "No text description.",
                "explanation": gq.get("explanation") or "",
                "subject_id": gq.get("subject_id")
            })
            
    # Natural sort by question_number
    try:
        def sort_key(q):
            num = q["question_number"]
            return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', num)]
        questions.sort(key=sort_key)
    except Exception:
        questions.sort(key=lambda x: x["question_number"])
        
    return questions

def get_options_by_question(question_id):
    """Fetches all options for a question_id."""
    result = supabase.table("gate_options")\
        .select("*")\
        .eq("question_id", question_id)\
        .execute()
    options = result.data
    options.sort(key=lambda x: x.get("option_label") or "")
    return options

def get_question_images(question_id):
    """Fetches all images for a question_id ordered by order_index."""
    result = supabase.table("gate_question_images")\
        .select("*")\
        .eq("question_id", question_id)\
        .order("order_index")\
        .execute()
    return result.data

def delete_question_images(question_id):
    """Deletes all existing images for a question."""
    return supabase.table("gate_question_images").delete().eq("question_id", question_id).execute()

def insert_question_image(question_id, image_url, order_index):
    """Inserts a new image record into gate_question_images."""
    return supabase.table("gate_question_images").insert({
        "question_id": question_id,
        "image_url": image_url,
        "order_index": order_index
    }).execute()

def get_option_images(option_id):
    """Fetches all images for a specific option_id ordered by order_index."""
    result = supabase.table("gate_option_images")\
        .select("*")\
        .eq("option_id", option_id)\
        .order("order_index")\
        .execute()
    return result.data

def delete_option_images(option_id):
    """Deletes all existing images for an option."""
    return supabase.table("gate_option_images").delete().eq("option_id", option_id).execute()

def insert_option_image(option_id, image_url, order_index):
    """Inserts a new image record into gate_option_images."""
    return supabase.table("gate_option_images").insert({
        "option_id": option_id,
        "image_url": image_url,
        "order_index": order_index
    }).execute()
