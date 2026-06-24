import os
from dotenv import load_dotenv
from scripts.resume_reader import read_resume
from scripts.job_matcher import calculate_match
from scripts.job_api_collector import collect_real_jobs
from scripts.skill_extractor import extract_skills
from scripts.job_database import clear_jobs, save_job

load_dotenv()

def run_matching_pipeline(resume_path_or_text="data/Resume.pdf", is_raw_text=False):
    """
    Wraps execution logic safely so it can be initiated via standard terminal 
    tasks OR hooked straight into dashboard handlers.
    """
    # Handle routing based on whether a path or raw text string is provided
    if not is_raw_text:
        if os.path.exists(resume_path_or_text):
            resume_text = read_resume(resume_path_or_text)
        else:
            # Fallback sample if file isn't found during CLI development checks
            resume_text = "Network Engineer Python Linux Networking Routing Switching Firewall"
    else:
        resume_text = resume_path_or_text

    # Extract dynamic resume properties
    extracted_skills = extract_skills(resume_text)
    
    # Refresh active operational databases
    clear_jobs()
    
    # Gather live market feeds
    raw_jobs = collect_real_jobs()
    
    for job in raw_jobs:
        score = calculate_match(resume_text, extracted_skills, job.get("description", ""))
        save_job(
            job_title=job.get("job_title"),
            company=job.get("company"),
            location=job.get("location"),
            description=job.get("description"),
            match_score=score,
            apply_url=job.get("apply_url")
        )
    print("Pipeline optimization workflow executed successfully!")

if __name__ == "__main__":
    # Traditional running script fallback
    run_matching_pipeline()