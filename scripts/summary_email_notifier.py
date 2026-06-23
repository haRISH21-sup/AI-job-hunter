import smtplib
import sqlite3
from email.message import EmailMessage


def get_watchlist_companies():

    try:

        conn = sqlite3.connect(
            "database/jobhunter.db"
        )

        cursor = conn.cursor()

        cursor.execute("""
        SELECT company
        FROM watchlist
        """)

        companies = [

            row[0].lower()

            for row in cursor.fetchall()
        ]

        conn.close()

        return companies

    except Exception:

        return []


def send_summary_email(
        sender_email,
        app_password,
        receiver_email,
        jobs
):

    if not jobs:

        print(
            "No high match jobs found."
        )

        return

    watchlist_companies = (
        get_watchlist_companies()
    )

    watchlist_matches = []

    body = (
        "\n===== AI JOB HUNTER DAILY SUMMARY =====\n\n"
    )

    body += (
        f"Total High Match Jobs: "
        f"{len(jobs)}\n\n"
    )

    body += (
        "=" * 60
        + "\n"
    )

    body += (
        "HIGH MATCH JOBS\n"
    )

    body += (
        "=" * 60
        + "\n\n"
    )

    for job in jobs:

        body += (

            f"Role: {job['job_title']}\n"

            f"Company: {job['company']}\n"

            f"Match Score: "
            f"{job['score']:.2f}%\n"

            f"Apply Link:\n"
            f"{job['apply_url']}\n"

            f"{'-'*60}\n"
        )

        if (
            job["company"]
            .lower()
            in watchlist_companies
        ):

            watchlist_matches.append(
                job
            )

    if watchlist_matches:

        body += "\n\n"

        body += (
            "=" * 60
            + "\n"
        )

        body += (
            "WATCHLIST ALERTS\n"
        )

        body += (
            "=" * 60
            + "\n\n"
        )

        for job in watchlist_matches:

            body += (

                f"WATCHLIST COMPANY FOUND!\n\n"

                f"Company: "
                f"{job['company']}\n"

                f"Role: "
                f"{job['job_title']}\n"

                f"Match Score: "
                f"{job['score']:.2f}%\n"

                f"Apply Link:\n"
                f"{job['apply_url']}\n"

                f"{'-'*60}\n"
            )

    msg = EmailMessage()

    msg["Subject"] = (

        f"AI Job Hunter Daily Summary "

        f"({len(jobs)} Jobs)"
    )

    msg["From"] = sender_email

    msg["To"] = receiver_email

    msg.set_content(
        body
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as smtp:

        smtp.login(
            sender_email,
            app_password
        )

        smtp.send_message(
            msg
        )

    print(
        f"Summary Email Sent "
        f"({len(jobs)} jobs)"
    )

    if watchlist_matches:

        print(
            f"Watchlist Alerts: "
            f"{len(watchlist_matches)}"
        )