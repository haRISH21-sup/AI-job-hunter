from scripts.database import (
    get_connection,
    initialize_database
)

from datetime import datetime


def save_job(
        job_title,
        company,
        location,
        description,
        match_score,
        apply_url
):

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO jobs
    (
        job_title,
        company,
        location,
        description,
        match_score,
        apply_url
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        job_title,
        company,
        location,
        description,
        float(match_score),
        apply_url
    ))

    cursor.execute("""
    INSERT INTO job_history
    (
        scan_date,
        job_title,
        company,
        location,
        match_score
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime(
            "%Y-%m-%d"
        ),
        job_title,
        company,
        location,
        float(match_score)
    ))

    conn.commit()
    conn.close()


def clear_jobs():

    initialize_database()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM jobs"
    )

    conn.commit()

    conn.close()


def view_jobs():

    initialize_database()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        job_title,
        company,
        location,
        match_score,
        apply_url
    FROM jobs
    ORDER BY match_score DESC
    LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    print(
        "\n===== TOP REAL JOB MATCHES =====\n"
    )

    for row in rows:

        print(
            f"Title: {row[0]}\n"
            f"Company: {row[1]}\n"
            f"Location: {row[2]}\n"
            f"Match: {float(row[3]):.2f}%\n"
            f"Apply Link: {row[4]}\n"
            f"{'-'*50}"
        )