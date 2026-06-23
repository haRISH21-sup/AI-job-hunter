from scripts.database import (
    get_connection,
    initialize_database
)


def add_company_to_watchlist(
        company
):

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        INSERT INTO watchlist
        (
            company
        )
        VALUES (?)
        """, (
            company,
        ))

        conn.commit()

    except:
        pass

    conn.close()


def get_watchlist():

    initialize_database()

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        company
    FROM watchlist
    ORDER BY company
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows