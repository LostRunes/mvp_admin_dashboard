import json

file_path = r"c:\flutter_projects\pyq_mvp\gate_import\os3_sample.json"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# We know the first object ends and second starts.
# Let's find the split point. Standard json module has JSONDecoder.raw_decode.
decoder = json.JSONDecoder()
content_stripped = content.strip()

# Decode the first JSON object
obj1, idx1 = decoder.raw_decode(content_stripped)

# Decode the second JSON object from where the first ended
remaining_content = content_stripped[idx1:].strip()
obj2, idx2 = decoder.raw_decode(remaining_content)

print("Object 1 keys:", list(obj1.keys()))
print("Object 1 questions count:", len(obj1.get("questions", [])))
print("Object 1 topics count:", len(obj1.get("topics", [])))

print("Object 2 keys:", list(obj2.keys()))
print("Object 2 questions count:", len(obj2.get("questions", [])))
print("Object 2 topics count:", len(obj2.get("topics", [])))

# Merge the structures
merged_obj = {
    "subject": obj1["subject"],  # Can keep Operating System
    "topics": obj1.get("topics", []) + obj2.get("topics", []),
    "questions": obj1.get("questions", []) + obj2.get("questions", [])
}

# Normalize subject name if desired
merged_obj["subject"]["subject_name"] = "Operating System"

# Deduplicate topics by topic_name
seen_topics = set()
deduped_topics = []
for topic in merged_obj["topics"]:
    name = topic.get("topic_name")
    if name not in seen_topics:
        seen_topics.add(name)
        deduped_topics.append(topic)
merged_obj["topics"] = deduped_topics

print("Merged questions count:", len(merged_obj["questions"]))
print("Merged topics count:", len(merged_obj["topics"]))

# Write back
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(merged_obj, f, indent=4, ensure_ascii=False)

print("Saved merged JSON successfully!")
