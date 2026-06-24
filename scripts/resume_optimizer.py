def optimize_resume(
        resume_skills,
        job_description
):

    suggestions = []

    missing_keywords = []

    keywords = [

        "Python",
        "Linux",
        "Windows",
        "Networking",
        "Cybersecurity",
        "TCP/IP",
        "Firewall",
        "SIEM",
        "SOC",
        "Azure",
        "AWS",
        "DNS",
        "DHCP",
        "Active Directory",
        "Incident Response",
        "Routing",
        "Switching",
        "Wireshark",
        "Nmap"

    ]

    job_lower = (
        job_description.lower()
    )

    for keyword in keywords:

        if (

            keyword.lower()
            in job_lower

            and

            keyword
            not in resume_skills

        ):

            missing_keywords.append(
                keyword
            )

    for keyword in missing_keywords:

        suggestions.append(

            f"Add experience or "
            f"projects related to "
            f"{keyword}"

        )

    return {

        "missing_keywords":
        missing_keywords,

        "suggestions":
        suggestions

    }