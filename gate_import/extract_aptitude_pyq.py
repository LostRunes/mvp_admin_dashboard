"""
extract_aptitude_pyq.py
Extracts GATE General Aptitude PYQ questions from a scanned PDF using Gemini Vision API.
Renders each page as an image, sends them in batches to Gemini, and assembles final JSON.
"""

import os
import json
import base64
import time
import fitz  # PyMuPDF
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io

load_dotenv()

PDF_PATH = "Aptitude_GATE_PYQ.pdf"
OUTPUT_JSON = "Aptitude_GeneralAptitude_PYQ.json"
CHAPTER_TOPIC = "General Aptitude"
SUBJECT_NAME = "General Aptitude"
SUBJECT_CODE = "GA"
DPI = 200
BATCH_SIZE = 4
SLEEP_BETWEEN_BATCHES = 6

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

SYSTEM_PROMPT = (
    "You are a GATE PYQ extraction assistant analyzing scanned book pages.\n\n"
    "I will give you one or more pages from a GATE General Aptitude previous-year-questions book.\n\n"
    "Your task: Extract EVERY question visible on these pages and return a JSON array of question objects.\n\n"
    "For each question return exactly this JSON object structure:\n"
    '{\n'
    '  "question_text": "...",\n'
    '  "question_type": "MCQ or MSQ or NAT",\n'
    '  "marks": 1,\n'
    '  "difficulty": "easy or medium or hard",\n'
    '  "concepts": ["specific concept tested"],\n'
    '  "tags": ["verbal ability", "sentence completion", "quantitative aptitude", "logical reasoning"],\n'
    '  "is_numerical": false,\n'
    '  "formula_based": false,\n'
    '  "estimated_solve_time_seconds": 60,\n'
    '  "options": [\n'
    '    {"label": "A", "text": "...", "is_correct": false},\n'
    '    {"label": "B", "text": "...", "is_correct": false},\n'
    '    {"label": "C", "text": "...", "is_correct": false},\n'
    '    {"label": "D", "text": "...", "is_correct": false}\n'
    '  ],\n'
    '  "correct_answer_text": null,\n'
    '  "explanation": "...",\n'
    '  "pyq_sources": [\n'
    '    {"year": 2022, "set": null, "question_number": "Q5", "marks": 1}\n'
    '  ]\n'
    '}\n\n'
    "CRITICAL RULES:\n"
    "- NAT questions: options=[] and correct_answer_text is the numerical answer as a string.\n"
    "- MCQ/MSQ: correct_answer_text=null. Mark correct option(s) with is_correct=true.\n"
    "- If explanation is absent from the book, return null for explanation.\n"
    "- marks: look for marks printed near the question (usually 1 or 2). Default 1 if unclear.\n"
    "- question_number: use number printed in book (e.g. Q4, Q1.7, 5).\n"
    "- year: extract from page header/footer. If not visible, use null.\n"
    "- set: use null unless multiple sets are shown (use integer 1,2,3).\n"
    "- tags: 3-8 searchable sub-topic tags (verbal ability, sentence completion, synonyms, antonyms,\n"
    "  reading comprehension, english grammar, quantitative aptitude, number series, data interpretation,\n"
    "  logical reasoning, analytical reasoning, spatial reasoning, etc.)\n"
    "- concepts: specific concept tested (e.g. Series Completion, Subject-Verb Agreement, Percentages)\n"
    "- Do NOT invent questions. Extract only what is printed on the pages.\n"
    "- Preserve mathematical expressions exactly as printed.\n"
    "- Remove page numbers, headers, footers from question_text.\n\n"
    "Return ONLY a valid JSON array. No markdown, no code blocks, no comments."
)


def pdf_pages_as_pil(pdf_path, dpi=200):
    doc = fitz.open(pdf_path)
    images = []
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)
        img_bytes = pix.tobytes("png")
        pil_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        images.append((page_num + 1, pil_img))
    doc.close()
    return images


def pil_to_gemini_part(pil_img):
    buf = io.BytesIO()
    pil_img.save(buf, format="JPEG", quality=85)
    data = buf.getvalue()
    return {"mime_type": "image/jpeg", "data": base64.b64encode(data).decode()}


def extract_questions_from_pages(page_images):
    parts = [SYSTEM_PROMPT]
    for page_num, img in page_images:
        parts.append("\n--- Page {} ---\n".format(page_num))
        parts.append(pil_to_gemini_part(img))

    response = model.generate_content(
        parts,
        generation_config=genai.GenerationConfig(temperature=0.1, max_output_tokens=8192)
    )
    text = response.text.strip()
    # Strip markdown fences if model wraps output
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:])
        if text.endswith("```"):
            text = text[:-3].strip()
    text = text.strip()
    return json.loads(text)


def merge_questions(all_questions):
    merged = {}
    for q in all_questions:
        key = q["question_text"].strip().lower()[:120]
        if key not in merged:
            merged[key] = dict(q)
        else:
            existing_sources = merged[key].get("pyq_sources", [])
            new_sources = q.get("pyq_sources", [])
            source_keys = {(s.get("year"), s.get("question_number")) for s in existing_sources}
            for src in new_sources:
                if (src.get("year"), src.get("question_number")) not in source_keys:
                    existing_sources.append(src)
            merged[key]["pyq_sources"] = existing_sources
    return list(merged.values())


def add_topic_field(questions, topic):
    for q in questions:
        q["topics"] = [topic]
    return questions


def build_final_json(questions):
    return {
        "subject": {"subject_name": SUBJECT_NAME, "subject_code": SUBJECT_CODE},
        "topics": [{
            "topic_name": CHAPTER_TOPIC,
            "summary": (
                "Covers verbal ability, English grammar, numerical aptitude, "
                "logical reasoning, and data interpretation as tested in the GATE General Aptitude section."
            )
        }],
        "questions": questions
    }


def main():
    print("[1/4] Rendering PDF pages from: {}".format(PDF_PATH))
    all_pages = pdf_pages_as_pil(PDF_PATH, dpi=DPI)
    print("      Total pages: {}".format(len(all_pages)))

    all_questions = []
    total_batches = (len(all_pages) + BATCH_SIZE - 1) // BATCH_SIZE
    print("[2/4] Extracting questions in {} batches of {} pages each...".format(total_batches, BATCH_SIZE))

    for batch_idx in range(total_batches):
        start = batch_idx * BATCH_SIZE
        end = min(start + BATCH_SIZE, len(all_pages))
        batch = all_pages[start:end]
        page_nums = [p[0] for p in batch]
        print("      Batch {}/{}: pages {} ...".format(batch_idx + 1, total_batches, page_nums), end=" ", flush=True)

        retries = 2
        for attempt in range(retries + 1):
            try:
                questions = extract_questions_from_pages(batch)
                print("got {} questions".format(len(questions)))
                all_questions.extend(questions)
                break
            except Exception as e:
                if attempt < retries:
                    print("retrying ({})...".format(attempt + 1), end=" ", flush=True)
                    time.sleep(10)
                else:
                    print("ERROR after {} attempts: {}".format(retries + 1, e))
                    partial_path = "partial_batch_{}.json".format(batch_idx + 1)
                    with open(partial_path, "w", encoding="utf-8") as f:
                        json.dump(all_questions, f, indent=2, ensure_ascii=False)
                    print("      Partial progress saved to {}".format(partial_path))

        if batch_idx < total_batches - 1:
            time.sleep(SLEEP_BETWEEN_BATCHES)

    print("[3/4] Deduplicating {} raw questions...".format(len(all_questions)))
    merged = merge_questions(all_questions)
    merged = add_topic_field(merged, CHAPTER_TOPIC)
    print("      After dedup: {} unique questions".format(len(merged)))

    print("[4/4] Writing output to: {}".format(OUTPUT_JSON))
    final = build_final_json(merged)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)

    print("\nDone! {} questions saved to {}".format(len(merged), OUTPUT_JSON))


if __name__ == "__main__":
    main()
