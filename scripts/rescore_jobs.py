"""
rescore_jobs.py

Rescores all jobs in the database against a given resume text.
Called from the dashboard when a user uploads their resume.
No API calls are made — it just re-evaluates existing jobs.
"""

from scripts.database import get_connection, initialize_database
from scripts.job_matcher import calculate_match


def rescore_jobs_for_resume(resume_text: str) -> int:
    """
    Takes resume_text, recalculates match_score for every job
    in the jobs table, and updates the DB in place.

    Returns the number of jobs rescored.
    """

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    # Fetch all jobs with their descriptions
    cursor.execute("""
        SELECT id, description
        FROM jobs
    """)

    rows = cursor.fetchall()

    if not rows:
        conn.close()
        return 0

    updated = 0

    for job_id, description in rows:

        if not description:
            continue

        new_score = calculate_match(
            resume_text,
            description
        )

        cursor.execute("""
            UPDATE jobs
            SET match_score = ?
            WHERE id = ?
        """, (float(new_score), job_id))

        updated += 1

    conn.commit()
    conn.close()

    return updated