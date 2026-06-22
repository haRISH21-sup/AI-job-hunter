import pandas as pd
import os

from scripts.database import (
    get_connection,
    initialize_database
)


def export_jobs_to_excel():

    initialize_database()

    conn = get_connection()

    query = """
    SELECT
        job_title,
        company,
        location,
        match_score,
        apply_url
    FROM jobs
    ORDER BY match_score DESC
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
        "output/jobs.xlsx"
    )

    df.to_excel(
        output_file,
        index=False
    )

    print(
        f"\nExcel Exported: {output_file}"
    )