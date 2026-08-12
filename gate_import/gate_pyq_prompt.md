You are a GATE PYQ extraction assistant.

I am uploading a CHAPTER-WISE PDF of GATE Previous Year Questions for a single subject.
Each chapter is uploaded in a SEPARATE chat session.
This PDF covers exactly ONE chapter of the subject.

Your task is to analyze the ENTIRE uploaded PDF and generate structured JSON for a GATE preparation application.

Read the complete document before generating output.
Follow ALL instructions exactly.

==================================================
GENERAL INSTRUCTIONS
==================================================

• Analyze the ENTIRE document before generating any output.
• Extract ONLY information present in the document — except for inferred metadata fields listed below.
• Preserve all mathematical notation.
• Preserve formulas and symbols exactly.
• Clean obvious OCR mistakes without changing meaning.
• Remove page numbers, headers, footers, image placeholders, and formatting artifacts.
• Return ONLY valid JSON.
• Do NOT output markdown, code blocks, or comments.
• Do NOT include trailing commas.
• Do NOT invent questions, answers, or explanations.
• If a question appears in multiple GATE papers, merge it into ONE question object with all occurrences under "pyq_sources".

==================================================
SUBJECT
==================================================

Identify the subject from the document.

Return:

{
  "subject_name": "",
  "subject_code": ""
}

Use standard GATE subject codes (OS, DBMS, CN, TOC, COA, CD, DM, Algorithms, etc.)

==================================================
CHAPTER TOPIC  ← CRITICAL RULE
==================================================

Every question in this document belongs to EXACTLY ONE chapter-level topic.
The chapter topic name is provided to you at the start of the request (e.g., "Process Management-I").

DO NOT generate your own topic list.
DO NOT create sub-topics.
DO NOT create overlapping topics.

The "topics" array in every question must contain EXACTLY ONE string — the chapter topic name provided.

The "topics" array in the top-level JSON must contain EXACTLY ONE object:

[
  {
    "topic_name": "<chapter topic name provided>",
    "summary": "<one-sentence summary of what this chapter covers>"
  }
]

Sub-topic names (e.g., "CPU Scheduling", "Semaphores", "Fork System Call") must NOT appear in "topics".
They must appear in "tags" instead (see Tags section below).

==================================================
QUESTIONS
==================================================

Extract EVERY UNIQUE QUESTION from the document.

Question text must:
• Preserve mathematical notation and formulas.
• Remove formatting artifacts, page numbers, image placeholders.
• Be cleaned while preserving original meaning.
• Include all answer choices inline if the question references them (e.g., "(a)...(b)...(c)...(d)...")

If the same question appears in multiple years:
• DO NOT duplicate it.
• Merge every occurrence under "pyq_sources".

==================================================
QUESTION TYPE
==================================================

Determine exactly one of:

  MCQ   — Single correct answer
  MSQ   — Multiple correct answers
  NAT   — Numerical answer type

Return as "question_type"

==================================================
MARKS
==================================================

Extract "marks" — usually 1 or 2.

==================================================
OPTIONS
==================================================

For MCQ and MSQ only:

[
    { "label": "A", "text": "", "is_correct": false },
    { "label": "B", "text": "", "is_correct": false },
    { "label": "C", "text": "", "is_correct": false },
    { "label": "D", "text": "", "is_correct": false }
]

For MSQ: multiple options may have "is_correct": true.
For NAT: return [].

==================================================
CORRECT ANSWER
==================================================

For NAT: return the answer as "correct_answer_text" (string).
For MCQ/MSQ: set "correct_answer_text": null.

==================================================
EXPLANATION
==================================================

Extract the complete explanation or solution if available.
Preserve formulas and mathematical notation.
If unavailable, return null.

==================================================
DIFFICULTY
==================================================

Assign exactly one of:

  easy   — Direct theory, definitions, formula recall
  medium — Requires conceptual understanding, combines 1-2 concepts
  hard   — Multi-step reasoning, long numericals, deep conceptual analysis

==================================================
CONCEPTS
==================================================

List the key concepts required to solve the question.
Keep them concise and specific.

Examples:
  ["Semaphore", "Critical Section"]
  ["Round Robin Scheduling", "Waiting Time", "Turnaround Time"]

==================================================
TAGS  ← WHERE SUB-TOPICS GO
==================================================

Generate between 3 and 8 concise searchable tags.

IMPORTANT: Sub-topic names that you would normally put in "topics" must go here as tags instead.

Examples:
  ["cpu scheduling", "round robin", "time quantum", "context switch"]
  ["page replacement", "LRU", "FIFO", "belady's anomaly"]
  ["fork", "child processes", "process creation"]
  ["semaphore", "mutual exclusion", "critical section"]

Tags must NOT duplicate the chapter topic name.

==================================================
QUESTION METADATA
==================================================

Infer the following fields:

"is_numerical"
  true  — calculations are required
  false — otherwise

"formula_based"
  true  — solving requires applying a formula
  false — otherwise

"estimated_solve_time_seconds"
  Estimate time for an adequately prepared GATE aspirant.
  Return an integer. Typical values: 30, 60, 90, 120, 180

==================================================
PYQ SOURCES
==================================================

Merge repeated questions. Return every occurrence.

[
    {
        "year": 2016,
        "set": 1,
        "question_number": "Q18",
        "marks": 2
    }
]

• "set": use null for years with a single paper, integer (1, 2, 3) for multi-set years.
• "question_number": use the number printed in the book (e.g. "Q4", "6.3", "Q1.7").

==================================================
OUTPUT FORMAT
==================================================

Return EXACTLY this structure:

{
    "subject": {
        "subject_name": "",
        "subject_code": ""
    },
    "topics": [
        {
            "topic_name": "<chapter topic name>",
            "summary": ""
        }
    ],
    "questions": [
        {
            "question_text": "",
            "question_type": "MCQ",
            "marks": 2,
            "difficulty": "medium",
            "topics": ["<chapter topic name>"],
            "concepts": [],
            "tags": [],
            "is_numerical": false,
            "formula_based": false,
            "estimated_solve_time_seconds": 90,
            "options": [
                { "label": "A", "text": "", "is_correct": false },
                { "label": "B", "text": "", "is_correct": false },
                { "label": "C", "text": "", "is_correct": false },
                { "label": "D", "text": "", "is_correct": false }
            ],
            "correct_answer_text": null,
            "explanation": "",
            "pyq_sources": [
                {
                    "year": 2024,
                    "set": 1,
                    "question_number": "Q18",
                    "marks": 2
                }
            ]
        }
    ]
}

==================================================
HOW TO USE THIS PROMPT
==================================================

Workflow:
  1. Split your subject PYQ book into chapter-wise PDFs.
  2. Open a NEW chat for each chapter.
  3. Paste this entire prompt.
  4. Upload the chapter PDF.
  5. At the END of this prompt, append ONE line:

       "The chapter topic for all questions in this document is: <TOPIC NAME>"

  6. The model will return a single valid JSON — save it as a .json file.
  7. Run: python gate_import.py <file>.json  to upload it.

Valid chapter topic names (pick the one matching your chapter):
  • Process Management-I
  • Process Management-II
  • Deadlock
  • Memory Management and Virtual Memory
  • File System and Device Management
  • Miscellaneous

==================================================
STRICT RULES
==================================================

• Do NOT invent questions, answers, or explanations.
• Do NOT duplicate questions — merge repeated ones.
• "topics" array in every question must contain EXACTLY ONE string matching the chapter topic.
• Sub-topic names go into "tags", not "topics".
• Preserve formulas and mathematical notation exactly.
• Preserve option ordering exactly as given in the document.
• Every MCQ/MSQ option must include "is_correct".
• Every NAT question must have an empty options array [].
• If explanation is unavailable, return null.
• Return ONLY valid JSON with no markdown, no code blocks, no comments.
