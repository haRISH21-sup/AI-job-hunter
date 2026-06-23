from collections import Counter


def generate_career_advice(
        resume_skills,
        jobs
):

    keywords = [

        "SIEM",
        "SOC",
        "Linux",
        "Windows",
        "Python",
        "Networking",
        "Firewall",
        "TCP/IP",
        "DNS",
        "DHCP",
        "Wireshark",
        "Nmap",
        "Incident Response",
        "Splunk",
        "QRadar",
        "Azure",
        "AWS",
        "Active Directory",
        "Routing",
        "Switching",
        "Cybersecurity"
    ]

    missing_skills = []

    for job in jobs:

        description = (
            job["description"]
            .lower()
        )

        for skill in keywords:

            if (
                skill.lower()
                in description
            ):

                if (
                    skill
                    not in resume_skills
                ):

                    missing_skills.append(
                        skill
                    )

    skill_counter = Counter(
        missing_skills
    )

    top_missing = [

        skill

        for skill, count

        in skill_counter.most_common(5)
    ]

    certifications = []

    if (
        "Routing" in top_missing
        or
        "Switching" in top_missing
    ):

        certifications.append(
            "CCNA"
        )

    if (
        "Firewall" in top_missing
    ):

        certifications.append(
            "Fortinet NSE"
        )

    if (
        "Cybersecurity" in top_missing
        or
        "SIEM" in top_missing
        or
        "SOC" in top_missing
    ):

        certifications.append(
            "CompTIA Security+"
        )

    if (
        "Azure" in top_missing
    ):

        certifications.append(
            "AZ-900"
        )

    if (
        "AWS" in top_missing
    ):

        certifications.append(
            "AWS Cloud Practitioner"
        )

    learning_scores = {

        "Networking": 0,
        "Security": 0,
        "Automation": 0,
        "Cloud": 0
    }

    for skill in top_missing:

        if skill in [

            "Routing",
            "Switching",
            "Networking",
            "TCP/IP",
            "DNS",
            "DHCP"

        ]:

            learning_scores[
                "Networking"
            ] += 20

        elif skill in [

            "SIEM",
            "SOC",
            "Firewall",
            "Cybersecurity",
            "Incident Response",
            "Splunk",
            "QRadar"

        ]:

            learning_scores[
                "Security"
            ] += 20

        elif skill in [

            "Python"
        ]:

            learning_scores[
                "Automation"
            ] += 20

        elif skill in [

            "Azure",
            "AWS"
        ]:

            learning_scores[
                "Cloud"
            ] += 20

    return {

        "top_missing":
        top_missing,

        "certifications":
        certifications,

        "learning_scores":
        learning_scores,

        "career_path": [

            "Network Engineer",

            "Network Security Engineer",

            "SOC Analyst",

            "Security Engineer"
        ]
    }