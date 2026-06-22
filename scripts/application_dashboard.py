from scripts.database import (
    get_connection,
    initialize_database
)


def show_dashboard():

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM applications"
    )
    total = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM applications
    WHERE status='Applied'
    """)
    applied = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM applications
    WHERE status='Interview'
    """)
    interview = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM applications
    WHERE status='Rejected'
    """)
    rejected = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM applications
    WHERE status='Offer'
    """)
    offer = cursor.fetchone()[0]

    conn.close()

    print("\n===== APPLICATION DASHBOARD =====\n")

    print(f"Total Applications : {total}")
    print(f"Applied            : {applied}")
    print(f"Interview          : {interview}")
    print(f"Rejected           : {rejected}")
    print(f"Offer              : {offer}")