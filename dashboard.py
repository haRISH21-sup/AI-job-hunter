import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

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
    """,
    conn
)

conn.close()

# ==========================
# APPLICATION STATISTICS
# ==========================

st.header("📋 Application Statistics")

col1, col2, col3, col4 = st.columns(4)

total_applications = len(
    applications
)

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
        total_applications
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

# ==========================
# JOB STATISTICS
# ==========================

st.header("💼 Job Statistics")

col1, col2, col3 = st.columns(3)

total_jobs = len(
    jobs
)

high_match_jobs = len(
    jobs[
        jobs["match_score"] >= 60
    ]
)

average_score = round(
    jobs["match_score"].mean(),
    2
)

with col1:
    st.metric(
        "Total Jobs",
        total_jobs
    )

with col2:
    st.metric(
        "Jobs Above 60%",
        high_match_jobs
    )

with col3:
    st.metric(
        "Average Match Score",
        f"{average_score}%"
    )

st.divider()

# ==========================
# TOP JOBS
# ==========================

st.header("🔥 Top Matching Jobs")

top_jobs = jobs.sort_values(
    by="match_score",
    ascending=False
)

st.dataframe(
    top_jobs.head(20),
    use_container_width=True
)

st.divider()

# ==========================
# COMPANY DISTRIBUTION
# ==========================

st.header("🏢 Top Hiring Companies")

company_counts = (
    jobs["company"]
    .value_counts()
    .reset_index()
)

company_counts.columns = [
    "Company",
    "Count"
]

fig_company = px.bar(
    company_counts.head(10),
    x="Company",
    y="Count",
    title="Top Hiring Companies"
)

st.plotly_chart(
    fig_company,
    use_container_width=True
)

st.divider()

# ==========================
# MATCH SCORE DISTRIBUTION
# ==========================

st.header("📊 Match Score Distribution")

fig_score = px.histogram(
    jobs,
    x="match_score",
    nbins=20,
    title="Job Match Scores"
)

st.plotly_chart(
    fig_score,
    use_container_width=True
)

st.divider()

# ==========================
# HIGH MATCH JOBS
# ==========================

st.header("⭐ Jobs Above 60% Match")

high_jobs = jobs[
    jobs["match_score"] >= 60
].sort_values(
    by="match_score",
    ascending=False
)

st.dataframe(
    high_jobs,
    use_container_width=True
)

st.divider()

# ==========================
# APPLICATION TABLE
# ==========================

st.header("📝 Applications")

st.dataframe(
    applications,
    use_container_width=True
)