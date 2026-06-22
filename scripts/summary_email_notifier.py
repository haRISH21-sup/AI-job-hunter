import smtplib
from email.message import EmailMessage


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

    body = (
        "\n===== AI JOB HUNTER DAILY SUMMARY =====\n\n"
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