from scripts.resume_reader import read_resume
from scripts.job_matcher import calculate_match
from scripts.job_api_collector import collect_real_jobs
from scripts.skill_extractor import extract_skills
from scripts.resume_generator import generate_resume

resume_text = read_resume(
    "resumes/Resume.pdf"
)

jobs = collect_real_jobs()

print("\n===== GENERATING ATS RESUMES =====\n")

generated = 0

for job in jobs:

    score = calculate_match(
        resume_text,
        job["description"]
    )

    if score < 60:
        continue

    skills = extract_skills(
        job["description"]
    )

    generate_resume(
        job["job_title"],
        job["company"],
        skills
    )

    print(
        f"{job['job_title']} | "
        f"{job['company']} | "
        f"{score}%"
    )

    generated += 1

    if generated >= 5:
        break

print(
    f"\nGenerated {generated} ATS resumes."
)