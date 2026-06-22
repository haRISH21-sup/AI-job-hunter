from scripts.database import get_connection, initialize_database


def save_job(
        job_title,
        company,
        location,
        description,
        match_score
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
        match_score
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        job_title,
        company,
        location,
        description,
        float(match_score)
    ))

    conn.commit()
    conn.close()


def clear_jobs():

    initialize_database()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("DELETE FROM jobs")

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
        match_score
    FROM jobs
    ORDER BY match_score DESC
    LIMIT 20
    """)

    rows = cursor.fetchall()

    conn.close()

    print("\n===== TOP REAL JOB MATCHES =====\n")

    for row in rows:

        print(
            f"{row[0]}\n"
            f"Company: {row[1]}\n"
            f"Location: {row[2]}\n"
            f"Match: {float(row[3]):.2f}%\n"
            f"{'-'*50}"
        )