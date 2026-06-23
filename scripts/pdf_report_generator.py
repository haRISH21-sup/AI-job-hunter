import os
import sqlite3

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_weekly_report():

    os.makedirs(
        "reports",
        exist_ok=True
    )

    pdf_file = (
        "reports/weekly_report.pdf"
    )

    conn = sqlite3.connect(
        "database/jobhunter.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM jobs"
    )
    total_jobs = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications"
    )
    total_applications = (
        cursor.fetchone()[0]
    )

    cursor.execute("""
    SELECT COUNT(*)
    FROM applications
    WHERE status='Interview'
    """)
    interviews = (
        cursor.fetchone()[0]
    )

    cursor.execute("""
    SELECT COUNT(*)
    FROM applications
    WHERE status='Offer'
    """)
    offers = (
        cursor.fetchone()[0]
    )

    cursor.execute("""
    SELECT COUNT(*)
    FROM applications
    WHERE status='Rejected'
    """)
    rejected = (
        cursor.fetchone()[0]
    )

    cursor.execute("""
    SELECT company,
           COUNT(*) as total
    FROM jobs
    GROUP BY company
    ORDER BY total DESC
    LIMIT 5
    """)

    top_companies = (
        cursor.fetchall()
    )

    conn.close()

    interview_rate = 0
    offer_rate = 0

    if total_applications > 0:

        interview_rate = round(
            (
                interviews
                / total_applications
            ) * 100,
            2
        )

        offer_rate = round(
            (
                offers
                / total_applications
            ) * 100,
            2
        )

    doc = SimpleDocTemplate(
        pdf_file
    )

    styles = (
        getSampleStyleSheet()
    )

    elements = []

    elements.append(
        Paragraph(
            "AI JOB HUNTER WEEKLY REPORT",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    report_lines = [

        f"Jobs Found: {total_jobs}",

        f"Applications: {total_applications}",

        f"Interviews: {interviews}",

        f"Offers: {offers}",

        f"Rejected: {rejected}",

        f"Interview Rate: {interview_rate}%",

        f"Offer Rate: {offer_rate}%"
    ]

    for line in report_lines:

        elements.append(
            Paragraph(
                line,
                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            "Top Companies",
            styles["Heading2"]
        )
    )

    for company, count in top_companies:

        elements.append(
            Paragraph(
                f"{company} ({count})",
                styles["BodyText"]
            )
        )

    doc.build(
        elements
    )

    print(
        f"PDF Report Created: {pdf_file}"
    )

    return pdf_file