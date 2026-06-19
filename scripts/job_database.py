from scripts.database import get_connection, initialize_database


def save_job(
        job_title,
        company,
        location,
        description,
        match_score
):

    initialize_database()

    match_score = float(match_score)

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
        match_score
    ))

    conn.commit()
    conn.close()

    print(f"Saved: {job_title}")


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
    """)

    rows = cursor.fetchall()

    conn.close()

    print("\n===== TOP MATCHING JOBS =====\n")

    if not rows:
        print("No Jobs Found")
        return

    for row in rows:

        print(
            f"Title: {row[0]}\n"
            f"Company: {row[1]}\n"
            f"Location: {row[2]}\n"
            f"Match Score: {float(row[3]):.2f}%\n"
            f"{'-'*40}"
        )