import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

from scripts.application_tracker import (
    update_status
)

from scripts.saved_jobs import (
    save_job_to_watchlist
)

from scripts.watchlist import (
    add_company_to_watchlist
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
        match_score,
        apply_url
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

saved_jobs = pd.read_sql_query(
    """
    SELECT *
    FROM saved_jobs
    """,
    conn
)

watchlist = pd.read_sql_query(
    """
    SELECT *
    FROM watchlist
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

col1.metric("New", new_count)
col2.metric("Applied", applied)
col3.metric("Interview", interview)
col4.metric("Rejected", rejected)
col5.metric("Offer", offer)

st.divider()

# =====================================
# SUCCESS METRICS
# =====================================

st.header("🎯 Success Metrics")

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

c1.metric(
    "Interview Rate",
    f"{interview_rate}%"
)

c2.metric(
    "Offer Rate",
    f"{offer_rate}%"
)

if not applications.empty:

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
# JOB FILTERS
# =====================================

st.header("🔍 Job Search Filters")

search_company = st.text_input(
    "Search Company"
)

search_job = st.text_input(
    "Search Job Title"
)

min_score = st.slider(
    "Minimum Match Score",
    0,
    100,
    50
)

filtered_jobs = jobs.copy()

if search_company:

    filtered_jobs = filtered_jobs[
        filtered_jobs["company"]
        .str.contains(
            search_company,
            case=False,
            na=False
        )
    ]

if search_job:

    filtered_jobs = filtered_jobs[
        filtered_jobs["job_title"]
        .str.contains(
            search_job,
            case=False,
            na=False
        )
    ]

filtered_jobs = filtered_jobs[
    filtered_jobs["match_score"] >= min_score
]

st.download_button(
    "📥 Download Filtered Jobs CSV",
    filtered_jobs.to_csv(
        index=False
    ),
    file_name="filtered_jobs.csv",
    mime="text/csv"
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
) if not jobs.empty else 0

col1.metric(
    "Total Jobs",
    total_jobs
)

col2.metric(
    "Jobs Above 60%",
    high_match_jobs
)

col3.metric(
    "Average Match Score",
    f"{average_score}%"
)

st.divider()

# =====================================
# MATCHING JOBS
# =====================================

st.header("🔥 Matching Jobs")

display_jobs = filtered_jobs.sort_values(
    by="match_score",
    ascending=False
)

st.dataframe(
    display_jobs,
    use_container_width=True
)

st.divider()

# =====================================
# APPLY + SAVE JOBS
# =====================================

st.header("🚀 Apply & Save Jobs")

for index, row in display_jobs.head(20).iterrows():

    col1, col2 = st.columns([5, 1])

    with col1:

        st.markdown(
            f"""
### {row['job_title']}
**Company:** {row['company']}  
**Location:** {row['location']}  
**Match Score:** {row['match_score']:.2f}%  

[Apply Now]({row['apply_url']})
"""
        )

    with col2:

        if st.button(
            "⭐ Save",
            key=f"save_{index}"
        ):

            save_job_to_watchlist(
                row["job_title"],
                row["company"],
                row["location"],
                row["match_score"],
                row["apply_url"]
            )

            st.success(
                "Job Saved"
            )

            st.rerun()

st.divider()

# =====================================
# WATCHLIST
# =====================================

st.header("⭐ Company Watchlist")

company_name = st.text_input(
    "Company Name"
)

if st.button(
    "Add To Watchlist"
):

    if company_name:

        add_company_to_watchlist(
            company_name
        )

        st.success(
            "Company Added"
        )

        st.rerun()

if not watchlist.empty:

    st.dataframe(
        watchlist,
        use_container_width=True
    )

st.divider()

# =====================================
# SAVED JOBS
# =====================================

st.header("⭐ Saved Jobs")

if not saved_jobs.empty:

    st.dataframe(
        saved_jobs,
        use_container_width=True
    )

    company_stats = (
        saved_jobs["company"]
        .value_counts()
        .reset_index()
    )

    company_stats.columns = [
        "Company",
        "Saved Jobs"
    ]

    fig_saved = px.bar(
        company_stats,
        x="Company",
        y="Saved Jobs",
        title="Most Saved Companies"
    )

    st.plotly_chart(
        fig_saved,
        use_container_width=True
    )

else:

    st.info(
        "No saved jobs yet."
    )

st.divider()

# =====================================
# JOB HISTORY ANALYTICS
# =====================================

st.header("📈 Job History Analytics")

if not history.empty:

    daily_jobs = (
        history.groupby(
            "scan_date"
        )
        .size()
        .reset_index(
            name="jobs_found"
        )
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

    avg_scores = (
        history.groupby(
            "scan_date"
        )["match_score"]
        .mean()
        .reset_index()
    )

    fig_avg = px.line(
        avg_scores,
        x="scan_date",
        y="match_score",
        title="Average Match Score Trend"
    )

    st.plotly_chart(
        fig_avg,
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

    col1.write(
        f"{row['company']} | {row['job_title']}"
    )

    statuses = [
        "New",
        "Applied",
        "Interview",
        "Rejected",
        "Offer"
    ]

    current_index = statuses.index(
        row["status"]
    )

    new_status = col2.selectbox(
        "Status",
        statuses,
        index=current_index,
        key=f"status_{index}"
    )

    if col3.button(
        "Update",
        key=f"btn_{index}"
    ):

        update_status(
            row["company"],
            row["job_title"],
            new_status
        )

        st.success(
            "Status Updated"
        )

        st.rerun()

st.divider()

# =====================================
# APPLICATION TABLE
# =====================================

st.header("📝 Applications")

st.dataframe(
    applications,
    use_container_width=True
)