from scripts.database import (
    get_connection,
    initialize_database
)

from datetime import datetime


def add_application(
        user_id,
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
            user_id,
            company,
            job_title,
            date_applied,
            status,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            user_id,
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
        user_id,
        company,
        job_title,
        status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE applications
    SET status=?
    WHERE user_id=?
    AND company=?
    AND job_title=?
    """, (
        status,
        user_id,
        company,
        job_title
    ))

    conn.commit()
    conn.close()


def get_applications(
        user_id
):

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
    WHERE user_id=?
    """, (
        user_id,
    ))

    rows = cursor.fetchall()

    conn.close()

    return rows


def view_applications():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        user_id,
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