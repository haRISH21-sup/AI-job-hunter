from scripts.database import (
    get_connection,
    initialize_database
)


def add_company_to_watchlist(
        user_id,
        company
):

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO watchlist
        (
            user_id,
            company
        )
        VALUES (?, ?)
        """, (
            user_id,
            company
        ))

        conn.commit()

    except:
        pass

    conn.close()


def get_watchlist(
        user_id
):

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        company
    FROM watchlist
    WHERE user_id=?
    ORDER BY company
    """, (
        user_id,
    ))

    rows = cursor.fetchall()

    conn.close()

    return rows