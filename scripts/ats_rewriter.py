def generate_summary(skills):

    skills_text = ", ".join(skills)

    summary = (
        "Network Engineer with hands-on experience in "
        "network monitoring, SIEM monitoring, Linux, "
        "Windows administration, firewall management, "
        "security monitoring and enterprise networking. "
        "Experienced with "
        + skills_text +
        ". Strong foundation in Cyber Security, "
        "SOC Operations, DNS, DHCP, Routing, "
        "Switching and Incident Analysis."
    )

    return summary


def prioritize_skills(skills):

    important = [
        "SIEM",
        "SOC",
        "Linux",
        "Cybersecurity",
        "Firewall",
        "Networking",
        "TCP/IP",
        "DNS",
        "DHCP",
        "Python"
    ]

    priority = []

    for item in important:
        if item in skills:
            priority.append(item)

    for item in skills:
        if item not in priority:
            priority.append(item)

    return priority