"""
Upload DBMS gate_year_analysis data from the image.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import supabase_utils

DBMS_SUBJECT_ID = "f38ec950-b35b-4e7e-9bed-75a6a3e2145f"

# (year, set_number, one_mark_ques, two_mark_ques, total_marks)
# "–" treated as 0 one-mark questions
YEAR_DATA = [
    (1997, None,  0, 2,  4),
    (1998, None,  2, 3,  8),
    (1999, None,  4, 3, 10),
    (2000, None,  2, 3,  8),
    (2001, None,  2, 2,  6),
    (2002, None,  2, 3,  8),
    (2003, None,  2, 3,  8),
    (2004, None,  2, 5, 12),
    (2005, None,  3, 4, 11),
    (2006, None,  1, 4,  9),
    (2007, None,  0, 6, 12),
    (2008, None,  1, 5, 11),
    (2009, None,  0, 5, 10),
    (2010, None,  2, 2,  6),
    (2011, None,  0, 2,  4),
    (2012, None,  2, 5, 12),
    (2013, None,  0, 3,  6),
    (2014,    1,  2, 3,  8),
    (2014,    2,  2, 3,  8),
    (2014,    3,  2, 3,  8),
    (2015,    1,  2, 2,  6),
    (2015,    2,  2, 2,  6),
    (2015,    3,  2, 2,  6),
    (2016,    1,  4, 1,  6),
    (2016,    2,  2, 2,  6),
    (2017,    1,  2, 3,  8),
    (2017,    2,  2, 3,  8),
    (2018, None,  2, 2,  6),
    (2019, None,  2, 3,  8),
    (2020, None,  2, 3,  8),
    (2021,    1,  2, 3,  8),
    (2021,    2,  2, 3,  8),
    (2022, None,  3, 2,  7),
    (2023, None,  1, 2,  5),
    (2024,    1,  4, 2,  8),
    (2024,    2,  4, 2,  8),
    (2025,    1,  2, 3,  8),
    (2025,    2,  1, 4,  9),
    (2026,    1,  2, 2,  6),
    (2026,    2,  2, 2,  6),
]

paper_cache = {}

def get_paper_id(year, set_number):
    key = (year, set_number)
    if key in paper_cache:
        return paper_cache[key]
    rows = supabase_utils.select("gate_papers", {"year": year, "set_number": set_number})
    if not rows:
        raise ValueError(f"No paper found for year={year}, set={set_number}")
    paper_cache[key] = rows[0]["id"]
    return rows[0]["id"]

inserted = skipped = 0
errors = []

print("Starting DBMS gate_year_analysis upload...\n")

for year, set_number, one_m, two_m, total in YEAR_DATA:
    label = f"{year} Set-{set_number}" if set_number else str(year)
    try:
        paper_id = get_paper_id(year, set_number)
        existing = supabase_utils.select("gate_year_analysis", {
            "paper_id": paper_id,
            "subject_id": DBMS_SUBJECT_ID,
        })
        if existing:
            print(f"  [SKIP]  {label}")
            skipped += 1
            continue
        supabase_utils.insert("gate_year_analysis", {
            "paper_id": paper_id,
            "subject_id": DBMS_SUBJECT_ID,
            "one_mark_questions": one_m,
            "two_mark_questions": two_m,
            "total_marks": total,
        })
        print(f"  [OK]    {label} — 1M={one_m}, 2M={two_m}, Total={total}")
        inserted += 1
    except Exception as e:
        print(f"  [ERROR] {label} — {e}")
        errors.append(label)

print(f"\n{'='*50}")
print(f"Done! Inserted: {inserted} | Skipped: {skipped} | Errors: {len(errors)}")
if errors:
    print(f"Failed: {errors}")
