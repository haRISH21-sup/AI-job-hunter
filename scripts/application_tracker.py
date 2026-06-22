from datetime import date

from scripts.database import (
    get_connection,
    initialize_database
)


def add_application(
        company,
        job_title,
        status="Applied",
        notes=""
):

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO applications
        (
            company,
            job_title,
            date_applied,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            company,
            job_title,
            str(date.today()),
            status,
            notes
        ))

        print("Application Added Successfully")

    except:

        print("Application Already Exists")

    conn.commit()
    conn.close()


def view_applications():

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        company,
        job_title,
        date_applied,
        status,
        notes
    FROM applications
    ORDER BY date_applied DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    print("\n===== APPLICATIONS =====\n")

    for row in rows:

        print(
            f"Company: {row[0]}\n"
            f"Job Title: {row[1]}\n"
            f"Date Applied: {row[2]}\n"
            f"Status: {row[3]}\n"
            f"Notes: {row[4]}\n"
            f"{'-'*40}"
        )


def update_status(
        company,
        job_title,
        new_status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET status = ?
    WHERE company = ?
    AND job_title = ?
    """, (
        new_status,
        company,
        job_title
    ))

    conn.commit()
    conn.close()

    print("Status Updated")