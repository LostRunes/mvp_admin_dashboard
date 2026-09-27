"""JSON importers — same inserts, in the same order, as CollegeJsonWorker / GateJsonWorker."""
import json


def _match(query, filters: dict):
    """Like .match(), but None becomes IS NULL instead of the invalid `eq.None`."""
    for k, v in filters.items():
        query = query.is_(k, "null") if v is None else query.eq(k, v)
    return query


def parse_json_upload(raw: bytes) -> dict:
    try:
        data = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ValueError(f"Not a valid UTF-8 JSON file: {e}") from None
    if not isinstance(data, dict):
        raise ValueError("JSON root must be an object with 'topics' and 'questions'.")
    return data


def import_college_json(log, sb, subject_id, data: dict) -> str:
    topics = data.get("topics", [])
    qs = data.get("questions", [])
    log(f"Importing: {len(topics)} topics, {len(qs)} questions")

    tm = {}
    for t in topics:
        r = sb.table("topics").insert({
            "subject_id": subject_id, "name": t["topic_name"], "summary": t.get("summary")
        }).execute()
        if r.data:
            tm[t["topic_name"]] = r.data[0]["id"]
            log(f"  Topic: {t['topic_name']}")

    for i, q in enumerate(qs):
        rq = sb.table("questions").insert({
            "question_text": q["question_text"], "difficulty": q.get("difficulty", "easy")
        }).execute()
        if not rq.data:
            continue
        qid = rq.data[0]["id"]

        for tn in q.get("topics", []):
            tid = tm.get(tn)
            if tid:
                sb.table("question_topics").insert({"question_id": qid, "topic_id": tid}).execute()

        for src in q.get("pyq_sources", []):
            ex = _match(sb.table("pyq_sources").select("id"), {**src, "subject_id": subject_id}).execute()
            pid = ex.data[0]["id"] if ex.data else (
                sb.table("pyq_sources").insert({**src, "subject_id": subject_id}).execute().data or [{}]
            )[0].get("id")
            if pid:
                sb.table("question_pyq_map").insert({"question_id": qid, "pyq_source_id": pid}).execute()
        log(f"  Q {i + 1}/{len(qs)}")
    log("✅ Done!")
    return f"College JSON Import complete! ({len(topics)} topics, {len(qs)} questions)"


def import_gate_json(log, sb, data: dict) -> str:
    sd = data.get("subject", {})
    topics = data.get("topics", [])
    qs = data.get("questions", [])
    log(f"Subject: {sd.get('subject_name')}")

    rs = sb.table("gate_subjects").select("*").eq("code", sd.get("subject_code")).execute()
    if rs.data:
        sid = rs.data[0]["id"]
    else:
        ri = sb.table("gate_subjects").insert({
            "name": sd.get("subject_name"), "code": sd.get("subject_code"), "display_order": 0
        }).execute()
        sid = ri.data[0]["id"]

    tm = {}
    for t in topics:
        rt = _match(sb.table("gate_topics").select("id"), {"subject_id": sid, "name": t["topic_name"]}).execute()
        if rt.data:
            tm[t["topic_name"]] = rt.data[0]["id"]
        else:
            ri = sb.table("gate_topics").insert({
                "subject_id": sid, "name": t["topic_name"], "summary": t.get("summary")
            }).execute()
            if ri.data:
                tm[t["topic_name"]] = ri.data[0]["id"]

    for i, q in enumerate(qs):
        rq = sb.table("gate_questions").insert({
            "subject_id": sid, "question_text": q["question_text"],
            "explanation": q.get("explanation"), "question_type": q.get("question_type", "MCQ"),
            "marks": q.get("marks", 1), "difficulty": q.get("difficulty", "easy")
        }).execute()
        if not rq.data:
            continue
        qid = rq.data[0]["id"]
        for tn in q.get("topics", []):
            tid = tm.get(tn)
            if tid:
                sb.table("gate_question_topics").insert({"question_id": qid, "topic_id": tid}).execute()
        for opt in q.get("options", []):
            sb.table("gate_options").insert({
                "question_id": qid, "option_label": opt.get("label"),
                "option_text": opt.get("text"), "is_correct": opt.get("is_correct", False)
            }).execute()
        for src in q.get("pyq_sources", []):
            paper = {"exam": src.get("exam", "GATE CSE"), "year": src["year"], "set_number": src.get("set")}
            rp = _match(sb.table("gate_papers").select("id"), paper).execute()
            if rp.data:
                pid = rp.data[0]["id"]
            else:
                ri2 = sb.table("gate_papers").insert(paper).execute()
                pid = ri2.data[0]["id"] if ri2.data else None
            if pid:
                sb.table("gate_question_occurrences").insert({
                    "question_id": qid, "paper_id": pid, "question_number": src["question_number"]
                }).execute()
        log(f"  Q {i + 1}/{len(qs)}")
    log("✅ Done!")
    return f"GATE import complete! ({len(qs)} questions)"
