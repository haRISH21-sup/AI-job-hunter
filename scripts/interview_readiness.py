def calculate_interview_readiness(
        resume_skills
):

    score = 0

    networking = 0
    security = 0
    automation = 0
    cloud = 0

    networking_skills = [

        "Networking",
        "TCP/IP",
        "DNS",
        "DHCP",
        "Routing",
        "Switching"

    ]

    security_skills = [

        "Firewall",
        "Cybersecurity",
        "SIEM",
        "SOC"

    ]

    automation_skills = [

        "Python"
    ]

    cloud_skills = [

        "AWS",
        "Azure",
        "Cloud"
    ]

    networking = sum(
        skill in resume_skills
        for skill in networking_skills
    ) * 15

    security = sum(
        skill in resume_skills
        for skill in security_skills
    ) * 20

    automation = sum(
        skill in resume_skills
        for skill in automation_skills
    ) * 25

    cloud = sum(
        skill in resume_skills
        for skill in cloud_skills
    ) * 15

    score = min(

        networking
        +
        security
        +
        automation
        +
        cloud,

        100
    )

    return {

        "overall":
        score,

        "networking":
        networking,

        "security":
        security,

        "automation":
        automation,

        "cloud":
        cloud
    }