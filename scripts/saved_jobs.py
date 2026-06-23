from scripts.database import (
    get_connection,
    initialize_database
)

from datetime import datetime


def save_job_to_watchlist(
        job_title,
        company,
        location,
        match_score,
        apply_url
):

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO saved_jobs
    (
        job_title,
        company,
        location,
        match_score,
        apply_url,
        saved_date
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        job_title,
        company,
        location,
        float(match_score),
        apply_url,
        datetime.now().strftime("%Y-%m-%d")
    ))

    conn.commit()
    conn.close()


def get_saved_jobs():

    initialize_database()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        job_title,
        company,
        location,
        match_score,
        apply_url,
        saved_date
    FROM saved_jobs
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows