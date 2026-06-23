from collections import Counter


def analyze_market(jobs_df):

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

    skill_counter = Counter()

    for _, row in jobs_df.iterrows():

        description = str(
            row.get(
                "description",
                ""
            )
        ).lower()

        for skill in skills_database:

            if skill.lower() in description:

                skill_counter[
                    skill
                ] += 1

    return dict(
        skill_counter.most_common(10)
    )