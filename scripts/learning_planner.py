def generate_learning_plan(
        missing_skills
):

    plan = []

    if (
        "Routing" in missing_skills
        or
        "Switching" in missing_skills
        or
        "Networking" in missing_skills
    ):

        plan.append(
            "Week 1 - CCNA Fundamentals"
        )

        plan.append(
            "Week 2 - Routing, Switching and VLANs"
        )

    if "Python" in missing_skills:

        plan.append(
            "Week 3 - Python Automation"
        )

    if (
        "Firewall" in missing_skills
        or
        "Cybersecurity" in missing_skills
    ):

        plan.append(
            "Week 4 - Network Security Fundamentals"
        )

    if (
        "SIEM" in missing_skills
        or
        "SOC" in missing_skills
    ):

        plan.append(
            "Week 5 - SIEM Fundamentals"
        )

        plan.append(
            "Week 6 - SOC Monitoring"
        )

    if (
        "AWS" in missing_skills
        or
        "Azure" in missing_skills
    ):

        plan.append(
            "Week 7 - Cloud Fundamentals"
        )

    if not plan:

        plan.append(
            "Resume is well aligned. Focus on interview preparation."
        )

    return plan