def remove_duplicate_jobs(jobs):

    unique_jobs = {}
    
    for job in jobs:

        key = (
            job["job_title"].strip().lower(),
            job["company"].strip().lower()
        )

        if key not in unique_jobs:
            unique_jobs[key] = job

    return list(unique_jobs.values())