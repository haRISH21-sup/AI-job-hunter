def extract_skills(resume_text):

    skills_database = [
        "Python",
        "Linux",
        "Windows",
        "Networking",
        "Cybersecurity",
        "TCP/IP",
        "Firewall",
        "OPNsense",
        "VMware",
        "Virtualization",
        "SIEM",
        "SOC",
        "Active Directory",
        "DNS",
        "DHCP",
        "Wireshark",
        "Nmap",
        "Switching",
        "Routing",
        "Cloud",
        "AWS",
        "Azure"
    ]

    found_skills = []

    resume_lower = resume_text.lower()

    for skill in skills_database:
        if skill.lower() in resume_lower:
            found_skills.append(skill)

    return found_skills