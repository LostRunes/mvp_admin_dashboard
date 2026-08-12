"""
Upload gate_year_analysis data extracted from the GATE paper analysis image.
Maps each row to an existing gate_papers record via (year, set_number),
then inserts into gate_year_analysis.

Table schema:
  id                uuid  PK
  paper_id          uuid  FK → gate_papers
  subject_id        uuid  FK → gate_subjects
  one_mark_questions  int
  two_mark_questions  int
  total_marks         int
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import supabase_utils

# ── Constants ────────────────────────────────────────────────────────────────
OS_SUBJECT_ID = "2b6e214e-ed0c-41d9-9d9a-9b8648420b0e"

# ── Data from image ──────────────────────────────────────────────────────────
# Each entry: (year, set_number, one_mark_ques, two_mark_ques, total_marks)
# set_number=None means single-paper year (no set suffix)
# 2005: "–" for 1-mark means 0 one-mark questions
YEAR_ANALYSIS_DATA = [
    # year  set   1M   2M   total
    (1997, None,  8,   2,   12),
    (1998, None,  8,   2,   12),
    (1999, None,  3,   3,    9),
    (2000, None,  1,   2,    5),
    (2001, None, 10,   3,   16),
    (2002, None,  2,   4,   10),
    (2003, None,  2,   5,   12),
    (2004, None,  3,   4,   11),
    (2005, None,  0,   2,    4),   # "–" treated as 0
    (2006, None,  1,   8,   17),
    (2007, None,  2,   6,   14),
    (2008, None,  2,   5,   12),
    (2009, None,  2,   5,   12),
    (2010, None,  3,   2,    7),
    (2011, None,  4,   2,    8),
    (2012, None,  1,   4,    9),
    (2013, None,  2,   4,   10),
    (2014,    1,  2,   3,    8),
    (2014,    2,  1,   3,    7),
    (2014,    3,  1,   3,    7),
    (2015,    1,  2,   4,   10),
    (2015,    2,  2,   3,    8),
    (2015,    3,  2,   2,    6),
    (2016,    1,  1,   4,    9),
    (2016,    2,  1,   3,    7),
    (2017,    1,  2,   2,    6),
    (2017,    2,  2,   2,    6),
    (2018, None,  2,   3,    8),
    (2019, None,  2,   4,   10),
    (2020, None,  2,   4,   10),
    (2021,    1,  4,   1,    6),
    (2021,    2,  1,   3,    7),
    (2022, None,  2,   4,   10),
    (2023, None,  3,   3,    9),
    (2024,    1,  2,   4,   10),
    (2024,    2,  2,   4,   10),
    (2025,    1,  2,   3,    8),
    (2025,    2,  1,   3,    7),
    (2026,    1,  2,   3,    8),
    (2026,    2,  1,   4,    9),
]


def fetch_paper_id(year, set_number):
    """Look up a gate_papers record by (year, set_number) and return its id."""
    result = supabase_utils.select("gate_papers", {
        "year": year,
        "set_number": set_number,
    })
    if not result:
        raise ValueError(
            f"No gate_papers record found for year={year}, set_number={set_number}. "
            "Please insert the paper first."
        )
    return result[0]["id"]


def main():
    print("Starting gate_year_analysis upload...\n")

    inserted = 0
    skipped = 0
    errors = []

    for year, set_number, one_m, two_m, total in YEAR_ANALYSIS_DATA:
        label = f"{year} Set-{set_number}" if set_number else str(year)
        try:
            # Check if record already exists for this paper + subject
            paper_id = fetch_paper_id(year, set_number)

            existing = supabase_utils.select("gate_year_analysis", {
                "paper_id": paper_id,
                "subject_id": OS_SUBJECT_ID,
            })

            if existing:
                print(f"  [SKIP]   {label} — already exists")
                skipped += 1
                continue

            # Insert new row
            supabase_utils.insert("gate_year_analysis", {
                "paper_id": paper_id,
                "subject_id": OS_SUBJECT_ID,
                "one_mark_questions": one_m,
                "two_mark_questions": two_m,
                "total_marks": total,
            })
            print(f"  [OK]     {label} — 1M={one_m}, 2M={two_m}, Total={total}")
            inserted += 1

        except ValueError as ve:
            print(f"  [WARN]   {label} — {ve}")
            errors.append(label)
        except Exception as e:
            print(f"  [ERROR]  {label} — {e}")
            errors.append(label)

    print(f"\n{'='*50}")
    print(f"Done! Inserted: {inserted} | Skipped: {skipped} | Errors: {len(errors)}")
    if errors:
        print(f"Failed rows: {errors}")


if __name__ == "__main__":
    main()
