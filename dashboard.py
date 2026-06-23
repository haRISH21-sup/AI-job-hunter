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

from scripts.career_coach import (
    generate_career_advice
)

from scripts.resume_reader import (
    read_resume
)

from scripts.skill_extractor import (
    extract_skills
)

from scripts.job_market_intelligence import (
    analyze_market
)

from scripts.application_reminder import (
    get_followup_jobs
)

from scripts.interview_readiness import (
    calculate_interview_readiness
)

from scripts.salary_intelligence import (
    get_salary_insights
)

from scripts.learning_planner import (
    generate_learning_plan
)

from scripts.mock_interview import (
    generate_mock_questions,
    evaluate_answers
)

from scripts.executive_dashboard import (
    generate_executive_summary
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
    description,
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
# RESUME PERFORMANCE ANALYTICS
# =====================================

st.header("📊 Resume Performance Analytics")

interview_rate = (
    round((interview / total) * 100, 2)
    if total > 0 else 0
)

offer_rate = (
    round((offer / total) * 100, 2)
    if total > 0 else 0
)

rejection_rate = (
    round((rejected / total) * 100, 2)
    if total > 0 else 0
)

success_rate = offer_rate

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Interview Rate",
    f"{interview_rate}%"
)

col2.metric(
    "Offer Rate",
    f"{offer_rate}%"
)

col3.metric(
    "Rejection Rate",
    f"{rejection_rate}%"
)

col4.metric(
    "Success Rate",
    f"{success_rate}%"
)

st.divider()

# =====================================
# APPLICATION FUNNEL
# =====================================

st.header("📈 Application Funnel")

funnel_df = pd.DataFrame({

    "Stage": [
        "Applications",
        "Interviews",
        "Offers"
    ],

    "Count": [
        total,
        interview,
        offer
    ]
})

fig_funnel = px.funnel(
    funnel_df,
    x="Count",
    y="Stage",
    title="Application Funnel"
)

st.plotly_chart(
    fig_funnel,
    use_container_width=True
)

st.divider()

# =====================================
# APPLICATION PIPELINE
# =====================================

st.header("📊 Application Pipeline")

pipeline_df = pd.DataFrame({

    "Status": [
        "New",
        "Applied",
        "Interview",
        "Rejected",
        "Offer"
    ],

    "Count": [
        new_count,
        applied,
        interview,
        rejected,
        offer
    ]
})

fig_pipeline = px.bar(
    pipeline_df,
    x="Status",
    y="Count",
    title="Application Pipeline"
)

st.plotly_chart(
    fig_pipeline,
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

if not watchlist.empty:

    watchlist_companies = [

        company.lower()

        for company in
        watchlist["company"]
    ]

    filtered_jobs["priority"] = (

        filtered_jobs["company"]
        .str.lower()
        .isin(
            watchlist_companies
        )

    )

    display_jobs = (
        filtered_jobs
        .sort_values(
            by=[
                "priority",
                "match_score"
            ],
            ascending=[
                False,
                False
            ]
        )
    )

else:

    display_jobs = (
        filtered_jobs
        .sort_values(
            by="match_score",
            ascending=False
        )
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
# WATCHLIST MATCHES TODAY
# =====================================

st.header("🚨 Watchlist Matches Today")

if not watchlist.empty:

    watchlist_companies = [

        company.lower()

        for company in
        watchlist["company"]
    ]

    watchlist_jobs = jobs[

        jobs["company"]
        .str.lower()
        .isin(
            watchlist_companies
        )

    ]

    if not watchlist_jobs.empty:

        watchlist_jobs = (
            watchlist_jobs
            .sort_values(
                by="match_score",
                ascending=False
            )
        )

        st.dataframe(
            watchlist_jobs,
            use_container_width=True
        )

        st.success(
            f"{len(watchlist_jobs)} "
            f"watchlist matches found."
        )

    else:

        st.info(
            "No watchlist matches "
            "found today."
        )

else:

    st.info(
        "Add companies to "
        "your watchlist first."
    )

st.divider()

# =====================================
# WATCHLIST ANALYTICS
# =====================================

st.header("📊 Watchlist Analytics")

if not watchlist.empty:

    watchlist_companies = [

        company.lower()

        for company in
        watchlist["company"]
    ]

    watchlist_jobs = jobs[

        jobs["company"]
        .str.lower()
        .isin(
            watchlist_companies
        )

    ]

    if not watchlist_jobs.empty:

        company_counts = (

            watchlist_jobs["company"]
            .value_counts()
            .reset_index()

        )

        company_counts.columns = [
            "Company",
            "Jobs Found"
        ]

        fig_watchlist = px.bar(
            company_counts,
            x="Company",
            y="Jobs Found",
            title="Watchlist Companies Found"
        )

        st.plotly_chart(
            fig_watchlist,
            use_container_width=True
        )

    else:

        st.info(
            "No watchlist company jobs found."
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
# AI CAREER COACH
# =====================================

st.header("🎯 AI Career Coach")

try:

    # Read Resume
    resume_text = read_resume(
        "resumes/Resume.pdf"
    )

    # Extract Skills
    resume_skills = extract_skills(
        resume_text
    )

    # Prepare Job Records
    job_records = []

    for _, row in jobs.iterrows():

        job_records.append({

            "description":
            str(
                row.get(
                    "description",
                    ""
                )
            )

        })

    # Generate Advice
    advice = (
        generate_career_advice(
            resume_skills,
            job_records
        )
    )

    col1, col2 = st.columns(2)

    # =====================
    # MISSING SKILLS
    # =====================

    with col1:

        st.subheader(
            "📚 Top Missing Skills"
        )

        if advice[
            "top_missing"
        ]:

            for skill in advice[
                "top_missing"
            ]:

                st.write(
                    f"• {skill}"
                )

        else:

            st.success(
                "No major skill gaps detected."
            )

    # =====================
    # CERTIFICATIONS
    # =====================

    with col2:

        st.subheader(
            "🎓 Recommended Certifications"
        )

        if advice[
            "certifications"
        ]:

            for cert in advice[
                "certifications"
            ]:

                st.write(
                    f"• {cert}"
                )

        else:

            st.success(
                "Current certifications appear sufficient."
            )

    # =====================
    # CAREER ROADMAP
    # =====================

    st.subheader(
        "🧭 Career Roadmap"
    )

    for step in advice[
        "career_path"
    ]:

        st.write(
            f"➡ {step}"
        )

    # =====================
    # CURRENT SKILLS
    # =====================

    st.subheader(
        "🛠 Current Resume Skills"
    )

    skill_df = pd.DataFrame({

        "Skills":
        resume_skills

    })

    st.dataframe(
        skill_df,
        use_container_width=True
    )

    # =====================
    # LEARNING PRIORITY
    # =====================

    st.subheader(
        "📊 Learning Priority"
    )

    score_df = pd.DataFrame({

        "Category":
        list(
            advice[
                "learning_scores"
            ].keys()
        ),

        "Score":
        list(
            advice[
                "learning_scores"
            ].values()
        )

    })

    fig_learning = px.bar(
        score_df,
        x="Category",
        y="Score",
        title="Learning Priority"
    )

    st.plotly_chart(
        fig_learning,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"Career Coach Error: {e}"
    )

st.divider()

# =====================================
# JOB MARKET INTELLIGENCE
# =====================================

st.header("📈 Job Market Intelligence")

try:

    market_skills = analyze_market(
        jobs
    )

    if market_skills:

        skill_df = pd.DataFrame({

            "Skill":
            list(
                market_skills.keys()
            ),

            "Demand":
            list(
                market_skills.values()
            )

        })

        st.subheader(
            "🔥 Top Skills In Demand"
        )

        fig_skills = px.bar(
            skill_df,
            x="Skill",
            y="Demand",
            title="Top Skills In Market"
        )

        st.plotly_chart(
            fig_skills,
            use_container_width=True
        )

        st.dataframe(
            skill_df,
            use_container_width=True
        )

    else:

        st.info(
            "No market skill data available."
        )

except Exception as e:

    st.warning(
        f"Market Intelligence Error: {e}"
    )

st.divider()

# =====================================
# TOP HIRING COMPANIES
# =====================================

st.header("🏢 Top Hiring Companies")

try:

    company_df = (

        jobs["company"]
        .value_counts()
        .head(10)
        .reset_index()

    )

    company_df.columns = [
        "Company",
        "Jobs"
    ]

    fig_company = px.bar(
        company_df,
        x="Company",
        y="Jobs",
        title="Top Hiring Companies"
    )

    st.plotly_chart(
        fig_company,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"Company Analytics Error: {e}"
    )

st.divider()

# =====================================
# TOP LOCATIONS
# =====================================

st.header("📍 Top Hiring Locations")

try:

    location_df = (

        jobs["location"]
        .value_counts()
        .head(10)
        .reset_index()

    )

    location_df.columns = [
        "Location",
        "Jobs"
    ]

    fig_location = px.bar(
        location_df,
        x="Location",
        y="Jobs",
        title="Top Hiring Locations"
    )

    st.plotly_chart(
        fig_location,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"Location Analytics Error: {e}"
    )

st.divider()

# =====================================
# APPLICATION REMINDERS
# =====================================

st.header("🔔 Follow-Up Reminders")

try:

    reminders = get_followup_jobs(
        applications
    )

    if reminders:

        reminder_df = pd.DataFrame(
            reminders
        )

        st.warning(
            f"{len(reminders)} applications "
            f"need follow-up."
        )

        st.dataframe(
            reminder_df,
            use_container_width=True
        )

        for reminder in reminders:

            st.info(

                f"Follow up with "
                f"{reminder['company']} "

                f"for "

                f"{reminder['job_title']} "

                f"({reminder['days']} days ago)"

            )

    else:

        st.success(
            "No follow-ups required."
        )

except Exception as e:

    st.warning(
        f"Reminder Error: {e}"
    )

st.divider()

# =====================================
# INTERVIEW READINESS SCORE
# =====================================

st.header("🎤 Interview Readiness Score")

try:

    resume_text = read_resume(
        "resumes/Resume.pdf"
    )

    resume_skills = extract_skills(
        resume_text
    )

    readiness = (
        calculate_interview_readiness(
            resume_skills
        )
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Overall",
        f"{readiness['overall']}%"
    )

    col2.metric(
        "Networking",
        f"{readiness['networking']}%"
    )

    col3.metric(
        "Security",
        f"{readiness['security']}%"
    )

    col4.metric(
        "Automation",
        f"{readiness['automation']}%"
    )

    col5.metric(
        "Cloud",
        f"{readiness['cloud']}%"
    )

    score_df = pd.DataFrame({

        "Category": [

            "Networking",
            "Security",
            "Automation",
            "Cloud"

        ],

        "Score": [

            readiness[
                "networking"
            ],

            readiness[
                "security"
            ],

            readiness[
                "automation"
            ],

            readiness[
                "cloud"
            ]
        ]
    })

    fig_readiness = px.bar(
        score_df,
        x="Category",
        y="Score",
        title="Interview Readiness Breakdown"
    )

    st.plotly_chart(
        fig_readiness,
        use_container_width=True
    )

    st.subheader(
        "📌 Recommendation"
    )

    if readiness["overall"] >= 80:

        st.success(
            "Interview Ready. Focus on mock interviews and advanced topics."
        )

    elif readiness["overall"] >= 60:

        st.warning(
            "Good foundation. Improve missing technical skills before interviews."
        )

    else:

        st.error(
            "Significant skill gaps detected. Focus on learning and certifications."
        )

except Exception as e:

    st.warning(
        f"Interview Readiness Error: {e}"
    )

st.divider()

# =====================================
# SALARY INTELLIGENCE
# =====================================

st.header("💰 Salary Intelligence")

try:

    resume_text = read_resume(
        "resumes/Resume.pdf"
    )

    resume_skills = extract_skills(
        resume_text
    )

    readiness = (
        calculate_interview_readiness(
            resume_skills
        )
    )

    salary_info = (
        get_salary_insights(
            readiness[
                "overall"
            ]
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Current Role",
            salary_info[
                "current_role"
            ]
        )

    with col2:

        st.metric(
            "Recommended Role",
            salary_info[
                "recommended_role"
            ]
        )

    with col3:

        st.metric(
            "Expected Salary",
            salary_info[
                "salary_range"
            ]
        )

    st.subheader(
        "📈 Career Growth Roadmap"
    )

    roadmap_df = pd.DataFrame({

        "Career Stage": [

            salary_info[
                "current_role"
            ],

            salary_info[
                "recommended_role"
            ],

            salary_info[
                "next_role"
            ]

        ],

        "Salary": [

            5,

            10,

            18

        ]

    })

    fig_salary = px.line(
        roadmap_df,
        x="Career Stage",
        y="Salary",
        markers=True,
        title="Salary Growth Roadmap (LPA)"
    )

    st.plotly_chart(
        fig_salary,
        use_container_width=True
    )

    st.subheader(
        "🎯 Career Recommendation"
    )

    st.info(

        f"Based on your interview readiness score of "

        f"{readiness['overall']}%, "

        f"your next target role should be "

        f"{salary_info['recommended_role']} "

        f"with an expected salary range of "

        f"{salary_info['salary_range']}."

    )

    st.subheader(
        "🚀 Next Career Step"
    )

    st.success(

        f"Target Role: "
        f"{salary_info['next_role']} | "

        f"Expected Salary: "
        f"{salary_info['next_salary']}"

    )

except Exception as e:

    st.warning(
        f"Salary Intelligence Error: {e}"
    )

st.divider()

# =====================================
# AUTO LEARNING PLANNER
# =====================================

st.header("📚 Auto Learning Planner")

try:

    resume_text = read_resume(
        "resumes/Resume.pdf"
    )

    resume_skills = extract_skills(
        resume_text
    )

    job_records = []

    for _, row in jobs.iterrows():

        job_records.append({

            "description":
            str(
                row.get(
                    "description",
                    ""
                )
            )

        })

    advice = generate_career_advice(
        resume_skills,
        job_records
    )

    learning_plan = (
        generate_learning_plan(
            advice[
                "top_missing"
            ]
        )
    )

    st.subheader(
        "🎯 Personalized Learning Roadmap"
    )

    for item in learning_plan:

        st.success(
            item
        )

    plan_df = pd.DataFrame({

        "Learning Plan":
        learning_plan

    })

    st.dataframe(
        plan_df,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"Learning Planner Error: {e}"
    )

st.divider()

# =====================================
# AI MOCK INTERVIEW
# =====================================

st.header("🎤 AI Mock Interview")

try:

    if "mock_questions" not in st.session_state:

        st.session_state.mock_questions = []

    if st.button(
        "Generate Mock Interview"
    ):

        st.session_state.mock_questions = (
            generate_mock_questions()
        )

    if st.session_state.mock_questions:

        answers = []

        st.subheader(
            "Interview Questions"
        )

        for i, question in enumerate(
            st.session_state.mock_questions
        ):

            st.write(
                f"Q{i+1}. {question}"
            )

            answer = st.text_area(
                f"Answer {i+1}",
                key=f"answer_{i}"
            )

            answers.append(
                answer
            )

        if st.button(
            "Evaluate Interview"
        ):

            result = (
                evaluate_answers(
                    answers
                )
            )

            st.metric(
                "Interview Score",
                f"{result['score']}%"
            )

            if result["score"] >= 80:

                st.success(
                    "Excellent Interview Performance"
                )

            elif result["score"] >= 60:

                st.warning(
                    "Good Performance - Improve Some Areas"
                )

            else:

                st.error(
                    "Needs Improvement"
                )

            st.subheader(
                "Feedback"
            )

            if result[
                "feedback"
            ]:

                for item in result[
                    "feedback"
                ]:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.success(
                    "All answers look detailed."
                )

except Exception as e:

    st.warning(
        f"Mock Interview Error: {e}"
    )

st.divider()

# =====================================
# EXECUTIVE DASHBOARD
# =====================================

st.header("📊 Executive Dashboard")

try:

    # Resume Skills
    resume_text = read_resume(
        "resumes/Resume.pdf"
    )

    resume_skills = extract_skills(
        resume_text
    )

    # Career Coach
    job_records = []

    for _, row in jobs.iterrows():

        job_records.append({

            "description":
            str(
                row.get(
                    "description",
                    ""
                )
            )

        })

    advice = generate_career_advice(
        resume_skills,
        job_records
    )

    # Interview Readiness
    readiness = (
        calculate_interview_readiness(
            resume_skills
        )
    )

    # Salary Intelligence
    salary_info = (
        get_salary_insights(
            readiness["overall"]
        )
    )

    # KPI Metrics
    total_jobs = len(jobs)

    applications_count = len(
        applications
    )

    interviews = len(

        applications[
            applications["status"]
            == "Interview"
        ]

    )

    offers = len(

        applications[
            applications["status"]
            == "Offer"
        ]

    )

    high_match_jobs = len(

        jobs[
            jobs["match_score"] >= 60
        ]

    )

    success_rate = 0

    if applications_count > 0:

        success_rate = round(

            (
                interviews
                +
                offers
            )
            /
            applications_count
            * 100,

            2

        )

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric(
        "Jobs",
        total_jobs
    )

    col2.metric(
        "High Match",
        high_match_jobs
    )

    col3.metric(
        "Applications",
        applications_count
    )

    col4.metric(
        "Interviews",
        interviews
    )

    col5.metric(
        "Offers",
        offers
    )

    col6.metric(
        "Success %",
        f"{success_rate}%"
    )

    st.divider()

    # Career Score

    career_score = round(

        (
            readiness["overall"]
            +
            success_rate
        ) / 2,

        2

    )

    st.metric(
        "🎯 Career Score",
        f"{career_score}%"
    )

    st.divider()

    # Executive Summary

    summary = (
        generate_executive_summary(

            readiness["overall"],

            salary_info,

            advice["top_missing"]

        )
    )

    st.subheader(
        "📋 Executive Summary"
    )

    st.info(
        summary
    )

    # Health Score

    health_df = pd.DataFrame({

        "Category": [

            "Interview Readiness",

            "Career Score",

            "Market Alignment",

            "Learning Progress"

        ],

        "Score": [

            readiness["overall"],

            career_score,

            80,

            75

        ]

    })

    fig_health = px.bar(

        health_df,

        x="Category",

        y="Score",

        title="Career Health Dashboard"

    )

    st.plotly_chart(
        fig_health,
        use_container_width=True
    )

except Exception as e:

    st.warning(
        f"Executive Dashboard Error: {e}"
    )

st.divider()

# =====================================
# APPLICATION TABLE
# =====================================

st.header("📝 Applications")

st.dataframe(
    applications,
    use_container_width=True
)