import os


def generate_cover_letter(
        company,
        job_title,
        skills
):

    os.makedirs(
        "generated_cover_letters",
        exist_ok=True
    )

    if isinstance(skills, list):
        skills = ", ".join(skills)

    cover_letter = f"""
Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company}.

My background includes experience with {skills}. I have worked on networking,
system administration, cybersecurity operations, monitoring, troubleshooting,
and security analysis projects.

I have hands-on experience with technologies such as Linux, Windows,
TCP/IP, Active Directory, DNS, DHCP, VMware, Firewall Management,
Network Monitoring, and Security Operations.

In addition, I developed an AI-powered Job Hunter platform using Python,
SQLite, NLP, APIs, and Streamlit which strengthened my automation,
problem-solving, and analytical skills.

I am eager to contribute to your team and would welcome the opportunity
to discuss how my skills align with your requirements.

Thank you for your time and consideration.

Sincerely,

Harish MR
"""

    filename = (
        f"generated_cover_letters/"
        f"{company}_{job_title}.txt"
    )

    filename = (
        filename
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            cover_letter
        )

    print(
        f"Cover Letter Generated: {filename}"
    )