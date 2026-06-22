from dotenv import load_dotenv
import os

from scripts.email_notifier import (
    send_job_alert
)

load_dotenv()

send_job_alert(
    os.getenv("EMAIL_SENDER"),
    os.getenv("EMAIL_PASSWORD"),
    os.getenv("EMAIL_RECEIVER"),
    "Test Company",
    "Network Engineer",
    95.5,
    "https://example.com/job"
)