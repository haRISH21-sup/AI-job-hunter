import pandas as pd
import os

from scripts.database import (
    get_connection,
    initialize_database
)


def export_applications_to_excel():

    initialize_database()

    conn = get_connection()

    query = """
    SELECT
        company,
        job_title,
        date_applied,
        status,
        notes
    FROM applications
    ORDER BY date_applied DESC
    """

    df = pd.read_sql_query(
        query,
        conn
    )

    conn.close()

    os.makedirs(
        "output",
        exist_ok=True
    )

    output_file = (
        "output/applications.xlsx"
    )

    df.to_excel(
        output_file,
        index=False
    )

    print(
        f"\nApplications Exported: {output_file}"
    )