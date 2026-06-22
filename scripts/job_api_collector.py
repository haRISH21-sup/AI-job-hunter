import requests
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")


def collect_real_jobs():

    searches = [
        "SOC Analyst",
        "Security Analyst",
        "Network Engineer",
        "NOC Engineer",
        "System Administrator",
        "Cyber Security"
    ]

    jobs = []

    for search in searches:

        print(f"Searching: {search}")

        url = (
            f"https://api.adzuna.com/v1/api/jobs/in/search/1"
            f"?app_id={APP_ID}"
            f"&app_key={APP_KEY}"
            f"&results_per_page=10"
            f"&what={search}"
            f"&content-type=application/json"
        )

        try:

            response = requests.get(
                url,
                timeout=15
            )

            print(
                f"Status Code: {response.status_code}"
            )

        except Exception as e:

            print(
                f"Error for {search}: {e}"
            )

            continue

        if response.status_code != 200:

            print(
                f"Failed Request for {search}"
            )

            continue

        try:

            data = response.json()

        except Exception as e:

            print(
                f"JSON Error for {search}: {e}"
            )

            continue

        if "results" not in data:

            print(
                f"No Results Key Found for {search}"
            )

            continue

        print(
            f"Jobs Found: {len(data['results'])}"
        )

        for job in data["results"]:

            jobs.append({
                "job_title": job.get(
                    "title",
                    ""
                ),
                "company": job.get(
                    "company",
                    {}
                ).get(
                    "display_name",
                    ""
                ),
                "location": job.get(
                    "location",
                    {}
                ).get(
                    "display_name",
                    ""
                ),
                "description": job.get(
                    "description",
                    ""
                ),
                "apply_url": job.get(
                    "redirect_url",
                    ""
                )
            })

    print(
        f"\nTotal Jobs Collected: {len(jobs)}"
    )

    return jobs