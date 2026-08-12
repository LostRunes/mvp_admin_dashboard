"""
remap_answers.py
----------------
Re-evaluates every aptitude question in the database by asking Gemini to
solve each question independently from the question text + options.
Updates:
  - aptitude_options.is_correct  (re-maps which option is correct)
  - aptitude_questions.explanation  (rewrites a clear, step-by-step explanation)

Usage:
    python remap_answers.py

Requirements:
    pip install supabase google-generativeai python-dotenv
"""

import os
import time
import json
import re
import warnings

# Suppress the FutureWarning from the deprecated google.generativeai package
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
from supabase import create_client
import google.generativeai as genai

# ---------------------------------------------------------
# LOAD CONFIG
# ---------------------------------------------------------
# 1. Load the local .env if it exists in the current folder (highest priority)
local_env = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".env")
)
if os.path.exists(local_env):
    load_dotenv(local_env)
    print(f"Loaded local env from {local_env}")

# 2. Load the primary supabase env as fallback
supabase_env = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "supabase", ".env")
)
if os.path.exists(supabase_env):
    load_dotenv(supabase_env, override=False)
    print(f"Loaded env from {supabase_env}")

# 3. Load the leetcode_uploader env as fallback
gemini_env = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "leetcode_uploader", ".env")
)
if os.path.exists(gemini_env):
    load_dotenv(gemini_env, override=False)
    print(f"Loaded Gemini key from {gemini_env}")

SUPABASE_URL = os.getenv("SOURCE_SUPABASE_URL", "https://hoihnpzdlivaoywrshmk.supabase.co")
SUPABASE_KEY = os.getenv("SOURCE_SUPABASE_SERVICE_KEY")
if not SUPABASE_KEY:
    SUPABASE_KEY = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhvaWhucHpkbGl2YW95d3JzaG1rIiwi"
        "cm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMwNzUyMCwiZXhwIjoyMDky"
        "ODgzNTIwfQ.yAOUceRqgb6mxcq_p9GDHhq34vriYlk2uZY-qOPOBsY"
    )

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY is not set. Add it to supabase/.env or leetcode_uploader/.env."
    )

genai.configure(api_key=GEMINI_API_KEY, transport='rest')
model = genai.GenerativeModel("gemini-flash-lite-latest")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# How many questions to process in a single run (None = all)
LIMIT = None
# Delay between Gemini calls (seconds) to respect rate limits
GEMINI_DELAY = 0.5


# ---------------------------------------------------------
# GEMINI SOLVER
# ---------------------------------------------------------
SYSTEM_PROMPT = """You are an expert aptitude test solver.
Given a multiple-choice aptitude question and its options, you must:
1. Carefully solve the question mathematically or logically.
2. Identify the single correct option (by its index, 0-based).
3. Write a concise, step-by-step explanation (3-6 sentences) that a student can follow.

Reply ONLY with valid JSON in this exact format (no markdown, no extra text):
{
  "correct_index": <0-based integer index of the correct option>,
  "explanation": "<clear step-by-step explanation>"
}"""


def ask_gemini(question_text, options):
    """
    Calls Gemini to solve the question.
    Returns {"correct_index": int, "explanation": str} or None on failure.
    """
    options_str = "\n".join(
        f"  {chr(65+i)}) {opt}" for i, opt in enumerate(options)
    )
    user_message = (
        f"Question:\n{question_text}\n\nOptions:\n{options_str}"
    )

    for attempt in range(5):
        try:
            print(f"    [DEBUG] Sending attempt {attempt+1}...")
            response = model.generate_content(
                SYSTEM_PROMPT + "\n\n" + user_message,
                request_options={'timeout': 15}
            )
            raw = response.text.strip()

            # Strip markdown code fences if present
            raw = re.sub(r"^```(?:json)?\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)

            parsed = json.loads(raw)
            idx = int(parsed["correct_index"])
            explanation = str(parsed["explanation"]).strip()

            if 0 <= idx < len(options):
                return {"correct_index": idx, "explanation": explanation}
            else:
                print(f"    [WARN] Gemini returned out-of-range index {idx} (options: {len(options)}). Skipping.")
                return None

        except json.JSONDecodeError as e:
            print(f"    [WARN] JSON parse error (attempt {attempt+1}): {e}")
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "ResourceExhausted" in err_msg or "quota" in err_msg.lower():
                delay = 30  # default sleep duration
                match = re.search(r"retry in (\d+\.?\d*)s", err_msg)
                if match:
                    delay = int(float(match.group(1))) + 2
                else:
                    match_sec = re.search(r"retryDelay': '(\d+)s'", err_msg)
                    if match_sec:
                        delay = int(match_sec.group(1)) + 2
                print(f"    [429 Rate Limit] Exceeded RPM quota. Sleeping for {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"    [WARN] Gemini error (attempt {attempt+1}): {e}")
                time.sleep(2)

    return None


# ---------------------------------------------------------
# MAIN REMAP LOGIC
# ---------------------------------------------------------
def main():
    # 1. Load completed question IDs from a local cache file to resume if restarted
    cache_file = os.path.join(os.path.dirname(__file__), "remapped_ids.txt")
    completed_ids = set()
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            for line in f:
                val = line.strip()
                if val:
                    completed_ids.add(int(val))
    print(f"Loaded {len(completed_ids)} already remapped questions from cache.\n")

    # 2. Fetch all topics
    topics_res = supabase.table("aptitude_topics").select("id, name").order("name").execute()
    topics = topics_res.data
    print(f"Found {len(topics)} topics.\n")

    total_processed = 0
    total_updated = 0
    total_skipped = 0
    total_errors = 0

    for topic in topics:
        topic_id = topic["id"]
        topic_name = topic["name"]
        print(f"\n--- Topic: {topic_name} (id={topic_id}) ---")

        # 2. Fetch questions + options for this topic
        q_res = (
            supabase.table("aptitude_questions")
            .select("id, question_text, aptitude_options(id, option_text, is_correct)")
            .eq("topic_id", topic_id)
            .order("id")
            .execute()
        )
        questions = q_res.data

        # Sort options by id so they appear in insertion order (A, B, C, D)
        for q in questions:
            if q.get("aptitude_options"):
                q["aptitude_options"].sort(key=lambda x: x["id"])

        if LIMIT is not None:
            questions = questions[:LIMIT]

        print(f"  Processing {len(questions)} questions...")

        for q_idx, q in enumerate(questions):
            q_id = q["id"]
            if q_id in completed_ids:
                continue
            q_text = q["question_text"]
            options_data = q.get("aptitude_options", [])

            if not options_data:
                print(f"  [Q{q_idx+1}] No options found - skipping.")
                total_skipped += 1
                continue

            option_texts = [o["option_text"] for o in options_data]

            total_processed += 1
            print(f"  [Q{q_idx+1}/{len(questions)}] Solving...")

            # 3. Ask Gemini to solve it
            result = ask_gemini(q_text, option_texts)
            time.sleep(GEMINI_DELAY)

            if result is None:
                print(f"  [Q{q_idx+1}] Gemini failed - skipping.")
                total_errors += 1
                continue

            correct_idx = result["correct_index"]
            explanation = result["explanation"]

            # 4. Update each option's is_correct flag
            all_updates_ok = True
            for i, opt in enumerate(options_data):
                should_be_correct = (i == correct_idx)
                if opt["is_correct"] == should_be_correct:
                    continue  # no change needed
                try:
                    supabase.table("aptitude_options") \
                        .update({"is_correct": should_be_correct}) \
                        .eq("id", opt["id"]) \
                        .execute()
                except Exception as e:
                    print(f"    [ERROR] Failed to update option id={opt['id']}: {e}")
                    all_updates_ok = False

            # 5. Update the explanation on the question
            try:
                supabase.table("aptitude_questions") \
                    .update({"explanation": explanation}) \
                    .eq("id", q_id) \
                    .execute()
            except Exception as e:
                print(f"    [ERROR] Failed to update explanation for question id={q_id}: {e}")
                all_updates_ok = False

            if all_updates_ok:
                correct_letter = chr(65 + correct_idx)
                print(
                    f"  [Q{q_idx+1}] OK  Correct -> {correct_letter}) {option_texts[correct_idx][:60]}"
                )
                total_updated += 1
                # Save to cache
                completed_ids.add(q_id)
                with open(cache_file, "a") as f:
                    f.write(f"{q_id}\n")
            else:
                total_errors += 1

    print("\n" + "=" * 60)
    print("REMAP SUMMARY")
    print("=" * 60)
    print(f"  Questions processed : {total_processed}")
    print(f"  Successfully updated: {total_updated}")
    print(f"  Skipped (no options): {total_skipped}")
    print(f"  Errors              : {total_errors}")
    print("=" * 60)


if __name__ == "__main__":
    start = time.time()
    main()
    print(f"\nCompleted in {time.time() - start:.1f}s")
