from scripts.resume_reader import read_resume
from scripts.job_collector import collect_jobs
from scripts.job_matcher import calculate_match
from scripts.job_database import save_job, view_jobs

resume_text = read_resume("resumes/Resume.pdf")

jobs = collect_jobs()

for _, job in jobs.iterrows():

    score = calculate_match(
        resume_text,
        job["description"]
    )

    save_job(
        job["job_title"],
        job["company"],
        job["location"],
        job["description"],
        score
    )

view_jobs()