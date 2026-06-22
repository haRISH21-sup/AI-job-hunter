import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

from scripts.application_tracker import (
    update_status
)

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

history = pd.read_sql_query(
    """
    SELECT
        scan_date,
        company,
        job_title,
        match_score
    FROM job_history
    """,
    conn
)

conn.close()

# =====================================
# APPLICATION STATISTICS
# =====================================

st.header("📋 Application Statistics")

new_count = len(
    applications[
        applications["status"] == "New"
    ]
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

rejected = len(
    applications[
        applications["status"] == "Rejected"
    ]
)

offer = len(
    applications[
        applications["status"] == "Offer"
    ]
)

total = len(applications)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("New", new_count)

with col2:
    st.metric("Applied", applied)

with col3:
    st.metric("Interview", interview)

with col4:
    st.metric("Rejected", rejected)

with col5:
    st.metric("Offer", offer)

st.divider()

# =====================================
# SUCCESS RATES
# =====================================

st.header("🎯 Application Success Metrics")

interview_rate = 0
offer_rate = 0

if total > 0:

    interview_rate = round(
        (interview / total) * 100,
        2
    )

    offer_rate = round(
        (offer / total) * 100,
        2
    )

c1, c2 = st.columns(2)

with c1:
    st.metric(
        "Interview Rate",
        f"{interview_rate}%"
    )

with c2:
    st.metric(
        "Offer Rate",
        f"{offer_rate}%"
    )

status_counts = (
    applications["status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Status",
    "Count"
]

fig_status = px.pie(
    status_counts,
    names="Status",
    values="Count",
    title="Application Status Distribution"
)

st.plotly_chart(
    fig_status,
    use_container_width=True
)

st.divider()

# =====================================
# JOB STATISTICS
# =====================================

st.header("💼 Job Statistics")

col1, col2, col3 = st.columns(3)

total_jobs = len(jobs)

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

st.header("🔥 Top Matching Jobs")

st.dataframe(
    jobs.sort_values(
        by="match_score",
        ascending=False
    ).head(20),
    use_container_width=True
)

st.divider()

st.header("📈 Job History Analytics")

if not history.empty:

    daily_jobs = (
        history.groupby("scan_date")
        .size()
        .reset_index(name="jobs_found")
    )

    fig_daily = px.line(
        daily_jobs,
        x="scan_date",
        y="jobs_found",
        title="Jobs Found Per Day"
    )

    st.plotly_chart(
        fig_daily,
        use_container_width=True
    )

st.divider()

# =====================================
# STATUS MANAGEMENT
# =====================================

st.header("🛠 Update Application Status")

for index, row in applications.iterrows():

    col1, col2, col3 = st.columns(
        [4, 2, 1]
    )

    with col1:

        st.write(
            f"{row['company']} | "
            f"{row['job_title']}"
        )

    with col2:

        new_status = st.selectbox(

            "Status",

            [
                "New",
                "Applied",
                "Interview",
                "Rejected",
                "Offer"
            ],

            index=[
                "New",
                "Applied",
                "Interview",
                "Rejected",
                "Offer"
            ].index(row["status"]),

            key=f"status_{index}"
        )

    with col3:

        if st.button(
            "Update",
            key=f"btn_{index}"
        ):

            update_status(
                row["company"],
                row["job_title"],
                new_status
            )

            st.success(
                "Updated"
            )

            st.rerun()

st.divider()

st.header("📝 Applications")

st.dataframe(
    applications,
    use_container_width=True
)