from scripts.database import (
    get_connection,
    initialize_database
)

from datetime import datetime


def add_application(
        company,
        job_title,
        status="New",
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
            datetime.now().strftime("%Y-%m-%d"),
            status,
            notes
        ))

        conn.commit()

    except:
        pass

    conn.close()


def update_status(
        company,
        job_title,
        status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET status=?
    WHERE company=?
    AND job_title=?
    """, (
        status,
        company,
        job_title
    ))

    conn.commit()
    conn.close()


def view_applications():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        company,
        job_title,
        date_applied,
        status
    FROM applications
    """)

    rows = cursor.fetchall()

    conn.close()

    for row in rows:
        print(row)