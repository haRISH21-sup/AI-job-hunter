import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(
    page_title="AI Job Hunter",
    layout="wide"
)

st.title("🚀 AI Job Hunter Dashboard")

conn = sqlite3.connect(
    "database/jobhunter.db"
)

applications = pd.read_sql_query(
    "SELECT * FROM applications",
    conn
)

jobs = pd.read_sql_query(
    """
    SELECT
        job_title,
        company,
        location,
        match_score
    FROM jobs
    ORDER BY match_score DESC
    LIMIT 20
    """,
    conn
)

conn.close()

st.header("Application Statistics")

col1, col2, col3, col4 = st.columns(4)

total = len(applications)

applied = len(
    applications[
        applications["status"] == "Applied"
    ]
)

interview = len(
    applications[
        applications["status"] == "Interview"
    ]
)

offer = len(
    applications[
        applications["status"] == "Offer"
    ]
)

with col1:
    st.metric(
        "Total Applications",
        total
    )

with col2:
    st.metric(
        "Applied",
        applied
    )

with col3:
    st.metric(
        "Interview",
        interview
    )

with col4:
    st.metric(
        "Offer",
        offer
    )

st.divider()

st.header("Top Matching Jobs")

st.dataframe(
    jobs,
    use_container_width=True
)

st.divider()

st.header("Applications")

st.dataframe(
    applications,
    use_container_width=True
)