"""
audit_and_fix.py
================
Reads all chapter JSONs from info.txt, checks if each question is in the DB
(matched by question_text + subject OS), verifies topic assignments,
and inserts/fixes anything that is missing or wrong.

RULE: Questions belong to ONLY the 6 chapter-level topics in gate_topics.
      Sub-topic names from each chapter's JSON go into gate_tags, not gate_topics.

Run from: c:\\flutter_projects\\pyq_mvp\\gate_import\\
"""

import sys
import re
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
import supabase_utils

# ── Config ────────────────────────────────────────────────────────────────────
INFO_TXT = os.path.join(os.path.dirname(__file__), "info.txt")
OS_SUBJECT_CODE = "OS"

# ── Counters ──────────────────────────────────────────────────────────────────
stats = {
    "chapters": 0,
    "questions_checked": 0,
    "questions_ok": 0,
    "questions_missing": 0,
    "questions_topic_fixed": 0,
    "questions_inserted": 0,
    "errors": [],
}

# ── Caches ────────────────────────────────────────────────────────────────────
subject_id_cache = {}
topic_id_cache = {}     # (subject_id, topic_name) -> id
paper_id_cache = {}     # (year, set_number) -> id
tag_id_cache = {}       # tag_name -> id


# ── Chapter → canonical topic name mapping ────────────────────────────────────
# ONLY these 6 topics are valid in gate_topics.
# All sub-topic names from each chapter JSON go into tags instead.
CHAPTER_TOPIC_MAP = {
    "ch1": "Process Management-I",
    "ch2": "Process Management-II",
    "ch3": "Deadlock",
    "ch4": "Memory Management and Virtual Memory",
    "ch5": "File System and Device Management",
    "ch6": "Miscellaneous",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

def fix_trailing_commas(s):
    """Remove trailing commas before ] or } (common JSON mistake)."""
    return re.sub(r',\s*([}\]])', r'\1', s)


def get_subject_id(code):
    if code in subject_id_cache:
        return subject_id_cache[code]
    rows = supabase_utils.select("gate_subjects", {"code": code})
    if not rows:
        raise ValueError(f"Subject with code '{code}' not found in DB.")
    subject_id_cache[code] = rows[0]["id"]
    return rows[0]["id"]


def get_or_create_topic(subject_id, topic_name):
    key = (subject_id, topic_name)
    if key in topic_id_cache:
        return topic_id_cache[key]
    topic, created = supabase_utils.get_or_create(
        "gate_topics",
        {"subject_id": subject_id, "name": topic_name},
    )
    if created:
        print(f"    [NEW TOPIC] Created chapter topic: '{topic_name}'")
    topic_id_cache[key] = topic["id"]
    return topic["id"]


def get_or_create_tag(tag_name):
    if tag_name in tag_id_cache:
        return tag_id_cache[tag_name]
    tag, _ = supabase_utils.get_or_create("gate_tags", {"name": tag_name})
    tag_id_cache[tag_name] = tag["id"]
    return tag["id"]


def get_paper_id(year, set_number):
    key = (year, set_number)
    if key in paper_id_cache:
        return paper_id_cache[key]
    rows = supabase_utils.select("gate_papers", {"year": year, "set_number": set_number})
    if not rows:
        new_paper, _ = supabase_utils.get_or_create(
            "gate_papers",
            {"exam": "GATE CSE", "year": year, "set_number": set_number}
        )
        paper_id_cache[key] = new_paper["id"]
        return new_paper["id"]
    paper_id_cache[key] = rows[0]["id"]
    return rows[0]["id"]


def find_existing_question(subject_id, question_text):
    """Look up question by subject_id + question_text."""
    rows = supabase_utils.select("gate_questions", {
        "subject_id": subject_id,
        "question_text": question_text,
    })
    return rows[0] if rows else None


def get_question_topic_ids(question_id):
    """Return set of topic_ids currently linked to a question."""
    rows = supabase_utils.select("gate_question_topics", {"question_id": question_id})
    return {r["topic_id"] for r in rows}


def get_question_tag_ids(question_id):
    """Return set of tag_ids currently linked to a question."""
    rows = supabase_utils.select("gate_question_tags", {"question_id": question_id})
    return {r["tag_id"] for r in rows}


def ensure_question_topics(question_id, chapter_topic_id):
    """Ensure the question is linked to its chapter topic."""
    existing = get_question_topic_ids(question_id)
    added = 0
    if chapter_topic_id not in existing:
        supabase_utils.insert("gate_question_topics", {
            "question_id": question_id,
            "topic_id": chapter_topic_id,
        })
        added += 1
    return added


def ensure_question_tags(question_id, tag_names):
    """Ensure all tags (including sub-topic names) are linked."""
    existing_tag_ids = get_question_tag_ids(question_id)
    added = 0
    for name in tag_names:
        if not name:
            continue
        tag_id = get_or_create_tag(name)
        if tag_id not in existing_tag_ids:
            supabase_utils.insert("gate_question_tags", {
                "question_id": question_id,
                "tag_id": tag_id,
            })
            existing_tag_ids.add(tag_id)
            added += 1
    return added


def insert_full_question(subject_id, q_data, chapter_topic_id, subtopic_names):
    """Insert a question and all related records."""
    fields = {
        "subject_id": subject_id,
        "question_text": q_data["question_text"],
        "question_type": q_data.get("question_type", "MCQ"),
        "difficulty": q_data.get("difficulty"),
        "marks": q_data.get("marks"),
        "explanation": q_data.get("explanation"),
        "correct_answer_text": q_data.get("correct_answer_text"),
        "is_numerical": q_data.get("is_numerical", False),
        "formula_based": q_data.get("formula_based", False),
        "estimated_solve_time_seconds": q_data.get("estimated_solve_time_seconds"),
    }
    res = supabase_utils.insert("gate_questions", fields)
    q_id = res[0]["id"]

    # Link to chapter-level topic ONLY
    supabase_utils.insert("gate_question_topics", {
        "question_id": q_id,
        "topic_id": chapter_topic_id,
    })

    # Tags: explicit tags + sub-topic names from JSON "topics" field
    all_tag_names = list(q_data.get("tags", [])) + subtopic_names
    seen = set()
    for tag_name in all_tag_names:
        if tag_name and tag_name not in seen:
            seen.add(tag_name)
            tag_id = get_or_create_tag(tag_name)
            supabase_utils.insert("gate_question_tags", {
                "question_id": q_id,
                "tag_id": tag_id,
            })

    # Options
    for opt in q_data.get("options", []):
        supabase_utils.insert("gate_options", {
            "question_id": q_id,
            "option_label": opt.get("label"),
            "option_text": opt.get("text"),
            "is_correct": opt.get("is_correct", False),
        })

    # Occurrences
    for src in q_data.get("pyq_sources", []):
        paper_id = get_paper_id(src.get("year"), src.get("set"))
        supabase_utils.insert("gate_question_occurrences", {
            "question_id": q_id,
            "paper_id": paper_id,
            "question_number": src.get("question_number"),
            "marks": src.get("marks", q_data.get("marks")),
        })

    return q_id


# ── Main ──────────────────────────────────────────────────────────────────────

def parse_chapters(path):
    """Return list of (chapter_label, ch_key, parsed_dict) from info.txt."""
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    header_pattern = r'(ch\d+\s*-[^\n\r]+)'
    parts = re.split(header_pattern, content, flags=re.IGNORECASE)

    chapters = []
    idx = 1
    while idx < len(parts) - 1:
        label = parts[idx].strip()
        body = parts[idx + 1].strip()
        idx += 2

        m = re.match(r'(ch\d+)', label, re.IGNORECASE)
        ch_key = m.group(1).lower() if m else None

        fixed_body = fix_trailing_commas(body)

        try:
            data = json.loads(fixed_body)
            chapters.append((label, ch_key, data))
        except json.JSONDecodeError as e:
            print(f"\n[WARN] Could not parse JSON for '{label}': {e}")
            stats["errors"].append(f"JSON parse failed: {label}")

    return chapters


def process_chapter(label, ch_key, data):
    subject_code = data.get("subject", {}).get("subject_code", OS_SUBJECT_CODE)
    subject_id = get_subject_id(subject_code)

    # Resolve the ONE chapter-level topic
    chapter_topic_name = CHAPTER_TOPIC_MAP.get(ch_key)
    if not chapter_topic_name:
        raise ValueError(f"No chapter topic mapping found for key '{ch_key}'")
    chapter_topic_id = get_or_create_topic(subject_id, chapter_topic_name)

    # Sub-topic names from chapter topics list (list of dicts)
    subtopic_names = [t["topic_name"] for t in data.get("topics", [])]

    questions = data.get("questions", [])
    print(f"\n{'='*60}")
    print(f"Chapter : {label}")
    print(f"Topic   : {chapter_topic_name}")
    print(f"SubTags : {len(subtopic_names)} | Questions: {len(questions)}")
    print(f"{'='*60}")

    for q_data in questions:
        stats["questions_checked"] += 1
        q_text = q_data.get("question_text", "").strip()
        short = q_text[:72].replace('\n', ' ') + ("..." if len(q_text) > 72 else "")

        # Sub-topics for this question — plain list of strings in the JSON
        q_subtopics = q_data.get("topics", [])  # already a list of strings

        existing = find_existing_question(subject_id, q_text)

        if existing:
            q_id = existing["id"]
            topic_added = ensure_question_topics(q_id, chapter_topic_id)
            tag_added = ensure_question_tags(q_id, q_subtopics)

            if topic_added > 0 or tag_added > 0:
                note = []
                if topic_added: note.append(f"+{topic_added} topic link")
                if tag_added:   note.append(f"+{tag_added} subtopic tags")
                print(f"  [FIXED] {short}")
                print(f"           {', '.join(note)}")
                stats["questions_topic_fixed"] += 1
            else:
                print(f"  [OK] {short}")
                stats["questions_ok"] += 1
        else:
            print(f"  [MISSING -> INSERT] {short}")
            try:
                insert_full_question(subject_id, q_data, chapter_topic_id, q_subtopics)
                stats["questions_inserted"] += 1
                print(f"    => Inserted OK")
            except Exception as e:
                msg = f"Insert failed: {short[:50]} | {e}"
                print(f"  [ERROR] {msg}")
                stats["errors"].append(msg)
                stats["questions_missing"] += 1


def main():
    print("=" * 60)
    print("GATE OS Question Audit & Fix Tool  (chapter-topics only)")
    print("=" * 60)

    chapters = parse_chapters(INFO_TXT)
    stats["chapters"] = len(chapters)
    print(f"\nParsed {len(chapters)} chapters from info.txt")
    print(f"Valid topics: {list(CHAPTER_TOPIC_MAP.values())}\n")

    for label, ch_key, data in chapters:
        try:
            process_chapter(label, ch_key, data)
        except Exception as e:
            msg = f"Chapter '{label}' failed: {e}"
            print(f"\n[ERROR] {msg}")
            stats["errors"].append(msg)

    print("\n")
    print("=" * 60)
    print("AUDIT SUMMARY")
    print("=" * 60)
    print(f"  Chapters processed : {stats['chapters']}")
    print(f"  Questions checked  : {stats['questions_checked']}")
    print(f"  Already correct    : {stats['questions_ok']}")
    print(f"  Fixed (topic/tag)  : {stats['questions_topic_fixed']}")
    print(f"  Newly inserted     : {stats['questions_inserted']}")
    print(f"  Failed             : {stats['questions_missing']}")
    if stats["errors"]:
        print(f"\n  Errors ({len(stats['errors'])}):")
        for e in stats["errors"]:
            print(f"    - {e}")
    else:
        print("\n  No errors encountered!")


if __name__ == "__main__":
    main()
