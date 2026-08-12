import os
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
from supabase import create_client

# ---------------------------------------------------------
# LOAD ENV VARIABLES AND CONFIG
# ---------------------------------------------------------
# Load environment variables from the shared supabase/.env file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "supabase", ".env"))
if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"Loaded environment variables from {env_path}")
else:
    print(f"Warning: {env_path} not found. Falling back to default environment variables.")

SUPABASE_URL = os.getenv("SOURCE_SUPABASE_URL", "https://hoihnpzdlivaoywrshmk.supabase.co")
SUPABASE_KEY = os.getenv("SOURCE_SUPABASE_SERVICE_KEY")

if not SUPABASE_KEY:
    # If the service key is not set, use the known hardcoded service key for supabase_primary
    SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvaWhucHpkbGl2YW95d3JzaG1rIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMwNzUyMCwiZXhwIjoyMDkyODgzNTIwfQ.yAOUceRqgb6mxcq_p9GDHhq34vriYlk2uZY-qOPOBsY"

print(f"Connecting to Supabase at: {SUPABASE_URL}")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 8 topics currently available on the Aptitude API
TOPICS = [
    {"name": "Mixture and Alligation", "slug": "MixtureAndAlligation"},
    {"name": "Profit and Loss", "slug": "ProfitAndLoss"},
    {"name": "Pipes and Cisterns", "slug": "PipesAndCistern"},
    {"name": "Age", "slug": "Age"},
    {"name": "Permutation and Combination", "slug": "PermutationAndCombination"},
    {"name": "Speed Time Distance", "slug": "SpeedTimeDistance"},
    {"name": "Simple Interest", "slug": "SimpleInterest"},
    {"name": "Calendars", "slug": "Calendar"},
]

# ---------------------------------------------------------
# OPTION MATCHING HELPER
# ---------------------------------------------------------
def find_correct_option_index(options, answer):
    """
    Finds the index of the correct option given the answer string.
    Employs exact, case-insensitive, numeric, and substring fallbacks.
    """
    if not options or not answer:
        return -1

    # 1. Exact match with whitespace stripped
    for i, opt in enumerate(options):
        if opt.strip() == answer.strip():
            return i

    # 2. Case-insensitive match with whitespace stripped
    for i, opt in enumerate(options):
        if opt.strip().lower() == answer.strip().lower():
            return i

    # 3. Numeric match (e.g. answer is "18" and option is "18 years" or vice versa)
    try:
        # Extract digits and decimal point
        ans_num = "".join(c for c in answer if c.isdigit() or c == '.')
        if ans_num:
            for i, opt in enumerate(options):
                opt_num = "".join(c for c in opt if c.isdigit() or c == '.')
                if opt_num and float(opt_num) == float(ans_num):
                    return i
    except ValueError:
        pass

    # 4. Substring containment match
    for i, opt in enumerate(options):
        if answer.strip().lower() in opt.strip().lower() or opt.strip().lower() in answer.strip().lower():
            return i

    # Default fallback
    return -1

# ---------------------------------------------------------
# API SCRAPER FOR A TOPIC
# ---------------------------------------------------------
def fetch_questions_for_topic(slug, max_unique=150, max_consecutive_duplicates=40, max_requests=600):
    """
    Fetches questions from the Aptitude API on a given topic slug.
    Since the API returns a single random question per hit, we call it in parallel
    batches and use duplicate detection to gather all questions.
    """
    url = f"https://aptitude-gold.vercel.app/{slug}"
    unique_questions = {}
    consecutive_duplicates = 0
    total_requests = 0
    batch_size = 8

    print(f"\nScraping topic '{slug}'...")

    with ThreadPoolExecutor(max_workers=4) as executor:
        while len(unique_questions) < max_unique and total_requests < max_requests:
            # Submit batch of asynchronous requests
            futures = [executor.submit(requests.get, url, timeout=10) for _ in range(batch_size)]
            
            for future in as_completed(futures):
                total_requests += 1
                try:
                    res = future.result()
                    if res.status_code == 200:
                        data = res.json()
                        q_text = data.get("question")
                        if not q_text:
                            continue
                        
                        # Clean question text to identify duplicates in memory
                        q_key = q_text.strip().lower()
                        if q_key not in unique_questions:
                            unique_questions[q_key] = data
                            consecutive_duplicates = 0  # Reset counter
                        else:
                            consecutive_duplicates += 1
                except Exception as e:
                    # Ignore networking errors, let the script keep running
                    pass

            # Print intermediate progress
            if total_requests % 40 == 0 or len(unique_questions) == max_unique:
                print(f"  [{slug}] Unique: {len(unique_questions)} | Total Requests: {total_requests} | Consecutive Duplicates: {consecutive_duplicates}")

            # If we hit the consecutive duplicate threshold, stop early
            if consecutive_duplicates >= max_consecutive_duplicates:
                print(f"  [{slug}] Stop condition hit: {consecutive_duplicates} consecutive duplicates. Collected almost all questions.")
                break

    print(f"Finished '{slug}': gathered {len(unique_questions)} questions from {total_requests} requests.")
    return list(unique_questions.values())

# ---------------------------------------------------------
# MAIN UPLOAD PROCESS
# ---------------------------------------------------------
def main():
    total_questions_scraped = 0
    total_questions_inserted = 0
    total_options_inserted = 0

    print("=========================================================")
    print("STARTING APTITUDE QUESTION UPLOADER")
    print("=========================================================")

    for topic_info in TOPICS:
        name = topic_info["name"]
        slug = topic_info["slug"]

        # 1. Fetch questions from Aptitude API
        scraped_data = fetch_questions_for_topic(slug)
        total_questions_scraped += len(scraped_data)
        
        if not scraped_data:
            print(f"No questions scraped for {name}. Skipping database updates.")
            continue

        # 2. Get or create topic in DB
        try:
            res = supabase.table("aptitude_topics").select("id").eq("slug", slug).execute()
            if res.data:
                topic_id = res.data[0]["id"]
                print(f"Topic '{name}' already exists in DB (ID: {topic_id}).")
            else:
                res_insert = supabase.table("aptitude_topics").insert({"name": name, "slug": slug}).execute()
                topic_id = res_insert.data[0]["id"]
                print(f"Created topic '{name}' in DB (ID: {topic_id}).")
        except Exception as e:
            print(f"Failed to resolve topic '{name}' in database. Error: {e}")
            continue

        # 3. Get existing questions in DB to prevent duplicates
        try:
            existing_res = supabase.table("aptitude_questions").select("question_text").eq("topic_id", topic_id).execute()
            existing_texts = {q["question_text"].strip().lower() for q in existing_res.data}
            print(f"Found {len(existing_texts)} existing questions for '{name}' in DB.")
        except Exception as e:
            print(f"Failed to load existing questions from DB: {e}")
            existing_texts = set()

        # 4. Prepare questions for insert
        questions_to_insert = []
        for q in scraped_data:
            q_text = q["question"]
            if q_text.strip().lower() not in existing_texts:
                questions_to_insert.append({
                    "topic_id": topic_id,
                    "question_text": q_text,
                    "explanation": q.get("explanation")
                })

        if not questions_to_insert:
            print(f"All scraped questions for '{name}' are already in the DB. No new records to insert.")
            continue

        # 5. Insert new questions in batches (Supabase returns inserted rows with IDs)
        print(f"Inserting {len(questions_to_insert)} new questions into DB...")
        try:
            inserted_questions = []
            # Batch size of 100 for safety and performance
            for i in range(0, len(questions_to_insert), 100):
                batch = questions_to_insert[i:i+100]
                res = supabase.table("aptitude_questions").insert(batch).execute()
                inserted_questions.extend(res.data)
            
            total_questions_inserted += len(inserted_questions)
            print(f"Successfully inserted {len(inserted_questions)} questions.")

            # Map from question_text -> inserted_id
            text_to_id = {q["question_text"].strip().lower(): q["id"] for q in inserted_questions}

            # 6. Prepare options for insert
            options_to_insert = []
            for q in scraped_data:
                q_text = q["question"]
                q_id = text_to_id.get(q_text.strip().lower())
                if not q_id:
                    # Skip if the question was not inserted (it already existed or insert failed)
                    continue

                options = q.get("options", [])
                answer = q.get("answer", "")
                correct_idx = find_correct_option_index(options, answer)

                for idx, opt in enumerate(options):
                    options_to_insert.append({
                        "question_id": q_id,
                        "option_text": opt,
                        "is_correct": (idx == correct_idx)
                    })

            # 7. Insert options in batches
            if options_to_insert:
                print(f"Inserting {len(options_to_insert)} options for new questions...")
                inserted_opts_count = 0
                for i in range(0, len(options_to_insert), 400):
                    opt_batch = options_to_insert[i:i+400]
                    res_opts = supabase.table("aptitude_options").insert(opt_batch).execute()
                    inserted_opts_count += len(res_opts.data)
                total_options_inserted += inserted_opts_count
                print(f"Successfully inserted {inserted_opts_count} options.")

        except Exception as e:
            print(f"Database insertion failed for topic '{name}': {e}")

    print("\n=========================================================")
    print("APTITUDE UPLOAD SUMMARY")
    print("=========================================================")
    print(f"Total questions scraped: {total_questions_scraped}")
    print(f"Total new questions inserted: {total_questions_inserted}")
    print(f"Total options inserted: {total_options_inserted}")
    print("=========================================================")

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"Completed in {time.time() - start_time:.2f} seconds.")
