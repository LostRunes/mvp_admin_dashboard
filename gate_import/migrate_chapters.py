"""
migrate_chapters.py

Migrates GATE OS questions from granular subtopics → 6 chapter-level topics.
Old subtopics become tags.

Steps:
  1. Snapshot: read all OS question-topic mappings
  2. Delete gate_question_topics for OS questions
  3. Delete gate_topics for OS
  4. Insert 6 new chapter topics
  5. Re-map questions → correct chapter (based on subtopic → chapter mapping)
  6. Add old subtopic names as tags (if not already tagged)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
import supabase_utils
import urllib.parse

OS_SUBJECT_ID = "2b6e214e-ed0c-41d9-9d9a-9b8648420b0e"

# === SUBTOPIC → CHAPTER MAPPING ===
CHAPTER_MAP = {
    # Process Management-I
    "Process Concept and States":       "Process Management-I",
    "Fork System Call":                 "Process Management-I",
    "Threads":                          "Process Management-I",
    "Multiprogramming":                 "Process Management-I",
    "CPU Scheduling Algorithms":        "Process Management-I",
    "Scheduling Numerical Problems":    "Process Management-I",
    "Job Scheduling":                   "Process Management-I",
    "Introduction and System Calls":    "Process Management-I",
    "I/O and Interrupts":               "Process Management-I",
    "I/O and Spooling":                 "Process Management-I",
    "Unix Signals and System Calls":    "Process Management-I",
    "Shell Commands":                   "Process Management-I",
    "Interrupts":                       "Process Management-I",

    # Process Management-II
    "Semaphores":                       "Process Management-II",
    "Race Condition":                   "Process Management-II",
    "Critical Section Problem":         "Process Management-II",
    "Peterson's Algorithm":             "Process Management-II",
    "Mutual Exclusion Algorithms":      "Process Management-II",
    "Producer-Consumer Problem":        "Process Management-II",
    "Readers-Writers Problem":          "Process Management-II",
    "Test-and-Set / Fetch-and-Add":     "Process Management-II",
    "Barrier Synchronization":          "Process Management-II",
    "Multithreading and Locks":         "Process Management-II",
    "Resource Allocation and Concurrency": "Process Management-II",
    "Process Synchronization":          "Process Management-II",

    # Deadlock
    "Deadlock":                         "Deadlock",
    "Deadlock Prevention":              "Deadlock",
    "Deadlock Avoidance":               "Deadlock",
    "Deadlock Detection and Recovery":  "Deadlock",
    "Deadlock and Starvation":          "Deadlock",
    "Necessary Conditions for Deadlock": "Deadlock",
    "Resource Allocation Graph":        "Deadlock",

    # Memory Management and Virtual Memory
    "Paging":                           "Memory Management and Virtual Memory",
    "Segmentation":                     "Memory Management and Virtual Memory",
    "Memory Allocation":                "Memory Management and Virtual Memory",
    "Virtual Memory":                   "Memory Management and Virtual Memory",
    "Virtual Memory and Paging":        "Memory Management and Virtual Memory",
    "Page Replacement Algorithms":      "Memory Management and Virtual Memory",
    "Demand Paging":                    "Memory Management and Virtual Memory",
    "TLB":                              "Memory Management and Virtual Memory",
    "Effective Access Time":            "Memory Management and Virtual Memory",
    "Multi-level Page Tables":          "Memory Management and Virtual Memory",
    "Inverted and Hashed Page Tables":  "Memory Management and Virtual Memory",
    "Memory Management Unit":           "Memory Management and Virtual Memory",
    "Fragmentation":                    "Memory Management and Virtual Memory",
    "Cache Memory":                     "Memory Management and Virtual Memory",
    "Belady's Anomaly":                 "Memory Management and Virtual Memory",
    "Linking and Loading":              "Memory Management and Virtual Memory",

    # File System and Device Management
    "File Allocation Methods":          "File System and Device Management",
    "Inode Structure and File Size Calculation": "File System and Device Management",
    "Directory Implementation":         "File System and Device Management",
    "Free Space Management":            "File System and Device Management",
    "Unix File System":                 "File System and Device Management",
    "Disk Scheduling":                  "File System and Device Management",
    "Disk Scheduling Algorithms":       "File System and Device Management",
    "Disk Capacity and Geometry":       "File System and Device Management",
}

CHAPTERS = [
    {"name": "Process Management-I",                "summary": "Introduction, Process, Threads & CPU Scheduling",    "display_order": 1},
    {"name": "Process Management-II",               "summary": "IPC, Synchronization and Concurrency",               "display_order": 2},
    {"name": "Deadlock",                            "summary": "Deadlock conditions, prevention, avoidance and detection", "display_order": 3},
    {"name": "Memory Management and Virtual Memory","summary": "Paging, Segmentation, Virtual Memory, Page Replacement, TLB", "display_order": 4},
    {"name": "File System and Device Management",   "summary": "File systems, disk scheduling, device management",   "display_order": 5},
    {"name": "Miscellaneous",                       "summary": "Miscellaneous OS topics",                            "display_order": 6},
]


def get_all_os_questions():
    """Fetch all OS questions."""
    return supabase_utils.select("gate_questions", f"subject_id=eq.{OS_SUBJECT_ID}&select=id,question_text")


def get_question_topic_mappings():
    """
    Returns: dict { question_id -> [topic_name, ...] }
    """
    url = (
        f"{supabase_utils.SUPABASE_URL}/rest/v1/gate_question_topics"
        f"?select=question_id,gate_topics(name)"
        f"&gate_topics.subject_id=eq.{OS_SUBJECT_ID}"
    )
    from config import HEADERS
    import requests
    res = requests.get(url, headers=HEADERS)
    rows = res.json()

    mappings = {}
    for row in rows:
        q_id = row["question_id"]
        topic_info = row.get("gate_topics")
        if topic_info and isinstance(topic_info, dict):
            name = topic_info.get("name")
            if name:
                mappings.setdefault(q_id, []).append(name)
    return mappings


def get_question_tag_names(question_id):
    """Get existing tag names for a question."""
    url = (
        f"{supabase_utils.SUPABASE_URL}/rest/v1/gate_question_tags"
        f"?question_id=eq.{question_id}&select=gate_tags(name)"
    )
    from config import HEADERS
    import requests
    res = requests.get(url, headers=HEADERS)
    rows = res.json()
    return {row["gate_tags"]["name"] for row in rows if row.get("gate_tags")}


def delete_os_question_topic_mappings():
    """Delete all gate_question_topics rows for OS questions."""
    # Build a list of OS question IDs
    questions = get_all_os_questions()
    q_ids = [q["id"] for q in questions]
    print(f"  Found {len(q_ids)} OS questions to unmap from old topics")

    from config import HEADERS
    import requests
    for qid in q_ids:
        url = f"{supabase_utils.SUPABASE_URL}/rest/v1/gate_question_topics?question_id=eq.{qid}"
        res = requests.delete(url, headers=HEADERS)
        if res.status_code not in (200, 204):
            print(f"  WARNING: Failed to delete topic mappings for question {qid}: {res.text}")

    print(f"  Deleted topic mappings for {len(q_ids)} questions")


def delete_os_topics():
    """Delete all gate_topics rows for the OS subject."""
    from config import HEADERS
    import requests
    url = f"{supabase_utils.SUPABASE_URL}/rest/v1/gate_topics?subject_id=eq.{OS_SUBJECT_ID}"
    res = requests.delete(url, headers=HEADERS)
    if res.status_code not in (200, 204):
        raise Exception(f"Failed to delete OS topics: {res.text}")
    print("  Deleted all old OS topics")


def insert_chapters():
    """Insert the 6 chapter topics and return {chapter_name -> id}."""
    chapter_ids = {}
    for ch in CHAPTERS:
        row, created = supabase_utils.get_or_create(
            "gate_topics",
            {"subject_id": OS_SUBJECT_ID, "name": ch["name"]},
            {"summary": ch["summary"], "display_order": ch["display_order"]}
        )
        chapter_ids[ch["name"]] = row["id"]
        status = "CREATED" if created else "EXISTING"
        print(f"  [{status}] Topic: {ch['name']}")
    return chapter_ids


def get_or_create_tag(tag_name, tag_cache):
    if tag_name in tag_cache:
        return tag_cache[tag_name]
    row, _ = supabase_utils.get_or_create("gate_tags", {"name": tag_name})
    tag_cache[tag_name] = row["id"]
    return row["id"]


def remap_questions_to_chapters(question_topic_map, chapter_ids):
    """
    For each question:
      - Determine which chapter(s) it belongs to based on old subtopics
      - Insert new gate_question_topics linking it to the chapter
      - Add old subtopic names as tags (if not already present)
    """
    from config import HEADERS
    import requests

    tag_cache = {}
    unmapped_questions = []  # questions with no recognized subtopics
    chapter_counts = {ch["name"]: 0 for ch in CHAPTERS}

    all_questions = get_all_os_questions()
    print(f"  Re-mapping {len(all_questions)} questions...")

    for q in all_questions:
        q_id = q["id"]
        old_topics = question_topic_map.get(q_id, [])
        chapters_for_q = set()

        for old_topic in old_topics:
            chapter = CHAPTER_MAP.get(old_topic, "Miscellaneous")
            chapters_for_q.add(chapter)

        # If question had no old topic mappings at all, put in Miscellaneous
        if not chapters_for_q:
            chapters_for_q = {"Miscellaneous"}
            unmapped_questions.append(q_id)

        # Insert chapter mappings
        for chapter_name in chapters_for_q:
            chapter_id = chapter_ids[chapter_name]
            res = supabase_utils.insert("gate_question_topics", {
                "question_id": q_id,
                "topic_id": chapter_id
            })
            chapter_counts[chapter_name] += 1

        # Add old subtopic names as tags
        existing_tags = get_question_tag_names(q_id)
        for old_topic in old_topics:
            if old_topic not in existing_tags:
                tag_id = get_or_create_tag(old_topic, tag_cache)
                supabase_utils.insert("gate_question_tags", {
                    "question_id": q_id,
                    "tag_id": tag_id
                })

    return chapter_counts, unmapped_questions


def main():
    print("\n[STEP 1] Snapshotting current question-topic mappings...")
    question_topic_map = get_question_topic_mappings()
    print(f"  Loaded topic mappings for {len(question_topic_map)} questions")

    print("\n[STEP 2] Deleting old OS question-topic mappings...")
    delete_os_question_topic_mappings()

    print("\n[STEP 3] Deleting old OS topics...")
    delete_os_topics()

    print("\n[STEP 4] Inserting 6 chapter topics...")
    chapter_ids = insert_chapters()

    print("\n[STEP 5] Re-mapping questions to chapters + adding subtopics as tags...")
    chapter_counts, unmapped = remap_questions_to_chapters(question_topic_map, chapter_ids)

    print("\n[DONE] Migration complete!")
    print("\nChapter question counts:")
    for name, count in chapter_counts.items():
        print(f"  {name}: {count}")
    if unmapped:
        print(f"\n  ⚠  {len(unmapped)} questions had no previous topic mapping → placed in Miscellaneous")


if __name__ == "__main__":
    main()
