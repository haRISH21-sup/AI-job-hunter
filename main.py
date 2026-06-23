import os
from dotenv import load_dotenv

from scripts.resume_reader import read_resume
from scripts.job_matcher import calculate_match
from scripts.job_api_collector import collect_real_jobs
from scripts.skill_extractor import extract_skills
from scripts.ats_rewriter import (
    generate_summary,
    prioritize_skills
)
from scripts.resume_generator import generate_resume
from scripts.docx_resume_generator import (
    generate_docx_resume
)
from scripts.cover_letter_generator import (
    generate_cover_letter
)
from scripts.docx_cover_letter_generator import (
    generate_docx_cover_letter
)
from scripts.interview_question_generator import (
    generate_interview_questions
)
from scripts.interview_answer_generator import (
    generate_interview_answers
)
from scripts.skill_gap_analyzer import (
    analyze_skill_gap
)
from scripts.ats_score_analyzer import (
    generate_ats_report
)
from scripts.application_package_generator import (
    create_application_package
)
from scripts.summary_email_notifier import (
    send_summary_email
)
from scripts.application_tracker import (
    add_application
)
from scripts.job_cleaner import (
    remove_duplicate_jobs
)
from scripts.job_database import (
    save_job,
    clear_jobs,
    view_jobs
)
from scripts.export_jobs import (
    export_jobs_to_excel
)
from scripts.pdf_report_generator import (
    generate_weekly_report
)

load_dotenv()

EMAIL_SENDER = os.getenv(
    "EMAIL_SENDER"
)

EMAIL_PASSWORD = os.getenv(
    "EMAIL_PASSWORD"
)

EMAIL_RECEIVER = os.getenv(
    "EMAIL_RECEIVER"
)

# Read Resume
resume_text = read_resume(
    "resumes/Resume.pdf"
)

# Extract Resume Skills
resume_skills = extract_skills(
    resume_text
)

# Clear Previous Scan Jobs
clear_jobs()

# Collect Jobs
jobs = collect_real_jobs()

# Remove Duplicates
jobs = remove_duplicate_jobs(
    jobs
)

print(
    f"\nUnique Jobs: {len(jobs)}"
)

generated = 0

high_match_jobs = []

print(
    "\n===== PROCESSING JOBS =====\n"
)

for job in jobs:

    score = calculate_match(
        resume_text,
        job["description"]
    )

    save_job(
        job["job_title"],
        job["company"],
        job["location"],
        job["description"],
        score,
        job["apply_url"]
    )

    if score >= 60:

        skills = extract_skills(
            job["description"]
        )

        prioritized_skills = prioritize_skills(
            skills
        )

        summary = generate_summary(
            prioritized_skills
        )

        generate_resume(
            job["job_title"],
            job["company"],
            summary,
            prioritized_skills
        )

        generate_docx_resume(
            job["job_title"],
            job["company"],
            summary,
            prioritized_skills
        )

        generate_cover_letter(
            job["company"],
            job["job_title"],
            prioritized_skills
        )

        generate_docx_cover_letter(
            job["company"],
            job["job_title"],
            prioritized_skills
        )

        generate_interview_questions(
            job["job_title"],
            job["company"]
        )

        generate_interview_answers(
            job["job_title"],
            job["company"]
        )

        analyze_skill_gap(
            job["company"],
            job["job_title"],
            resume_skills,
            job["description"]
        )

        generate_ats_report(
            job["company"],
            job["job_title"],
            resume_skills,
            job["description"],
            score
        )

        create_application_package(
            job["company"],
            job["job_title"]
        )

        # AUTO APPLICATION TRACKER
        add_application(
            job["company"],
            job["job_title"],
            "New"
        )

        high_match_jobs.append({

            "job_title":
            job["job_title"],

            "company":
            job["company"],

            "score":
            score,

            "apply_url":
            job["apply_url"]

        })

        generated += 1

print(
    f"\nGenerated {generated} ATS resumes."
)

view_jobs()

export_jobs_to_excel()
pdf_report = (
    generate_weekly_report()
)

try:

    send_summary_email(

    EMAIL_SENDER,

    EMAIL_PASSWORD,

    EMAIL_RECEIVER,

    high_match_jobs,

    pdf_report
)
except Exception as e:

    print(
        f"Summary Email Failed: {e}"
    )