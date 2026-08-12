"""
update_json_files.py

Updates os_sample.json, os2_sample.json, os3_sample.json:
- Replaces "topics" array with 6 chapter topics
- In each question, maps "topics": [subtopic_names] → [chapter_name]
- Appends old subtopic names to "tags" (deduplicated)
"""

import json
import os

CHAPTER_MAP = {
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

    "Deadlock":                         "Deadlock",
    "Deadlock Prevention":              "Deadlock",
    "Deadlock Avoidance":               "Deadlock",
    "Deadlock Detection and Recovery":  "Deadlock",
    "Deadlock and Starvation":          "Deadlock",
    "Necessary Conditions for Deadlock": "Deadlock",
    "Resource Allocation Graph":        "Deadlock",

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

    "File Allocation Methods":          "File System and Device Management",
    "Inode Structure and File Size Calculation": "File System and Device Management",
    "Directory Implementation":         "File System and Device Management",
    "Free Space Management":            "File System and Device Management",
    "Unix File System":                 "File System and Device Management",
    "Disk Scheduling":                  "File System and Device Management",
    "Disk Scheduling Algorithms":       "File System and Device Management",
    "Disk Capacity and Geometry":       "File System and Device Management",
}

CHAPTERS_TOPICS = [
    {"topic_name": "Process Management-I",                "summary": "Introduction, Process, Threads & CPU Scheduling", "display_order": 1},
    {"topic_name": "Process Management-II",               "summary": "IPC, Synchronization and Concurrency",            "display_order": 2},
    {"topic_name": "Deadlock",                            "summary": "Deadlock conditions, prevention, avoidance and detection", "display_order": 3},
    {"topic_name": "Memory Management and Virtual Memory","summary": "Paging, Segmentation, Virtual Memory, Page Replacement, TLB", "display_order": 4},
    {"topic_name": "File System and Device Management",   "summary": "File systems, disk scheduling, device management", "display_order": 5},
    {"topic_name": "Miscellaneous",                       "summary": "Miscellaneous OS topics",                        "display_order": 6},
]


def update_question(q):
    old_topics = q.get("topics", [])
    old_tags = q.get("tags", [])

    # Map old subtopics → chapter names (deduplicated)
    chapters = list(dict.fromkeys(
        CHAPTER_MAP.get(t, "Miscellaneous") for t in old_topics
    ))
    if not chapters:
        chapters = ["Miscellaneous"]

    # Add old subtopic names to tags (if not already there)
    tags_set = list(old_tags)
    tags_lower = {t.lower() for t in tags_set}
    for old_topic in old_topics:
        if old_topic.lower() not in tags_lower:
            tags_set.append(old_topic)
            tags_lower.add(old_topic.lower())

    q["topics"] = chapters
    q["tags"] = tags_set
    return q


def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Replace topics array with 6 chapters
    data["topics"] = CHAPTERS_TOPICS

    # Update each question
    questions = data.get("questions", [])
    for i, q in enumerate(questions):
        questions[i] = update_question(q)
    data["questions"] = questions

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"  Updated {path}: {len(questions)} questions")


FILES = [
    "os_sample.json",
    "os2_sample.json",
    "os3_sample.json",
]

for fname in FILES:
    fpath = os.path.join(os.path.dirname(__file__), fname)
    print(f"\nProcessing {fname}...")
    process_file(fpath)

print("\n[DONE] All JSON files updated.")
