from scripts.database import (
    get_connection,
    initialize_database
)

from datetime import datetime


def add_recruiter(
        user_id,
        recruiter_name,
        company,
        email,
        linkedin,
        status,
        notes=""
):

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO recruiters (

        user_id,
        recruiter_name,
        company,
        email,
        linkedin,
        status,
        notes,
        last_contact

    )

    VALUES (?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        user_id,
        recruiter_name,
        company,
        email,
        linkedin,
        status,
        notes,

        datetime.now().strftime(
            "%Y-%m-%d"
        )

    ))

    conn.commit()
    conn.close()


def get_recruiters(
        user_id
):

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""

    SELECT
        recruiter_name,
        company,
        email,
        linkedin,
        status,
        notes,
        last_contact

    FROM recruiters

    WHERE user_id=?

    """, (
        user_id,
    ))

    rows = cursor.fetchall()

    conn.close()

    return rows