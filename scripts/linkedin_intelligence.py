def generate_linkedin_profile(
        resume_skills
):

    headline = (

        "Network Engineer | "

        "Python Automation | "

        "Network Security | "

        "CCNA"

    )

    about = (

        "Network Engineer with hands-on "

        "experience in networking, "

        "routing, switching, monitoring, "

        "firewall administration, "

        "Python automation, and "

        "cybersecurity fundamentals. "

        "Passionate about network "

        "security, SOC operations, "

        "and infrastructure automation."

    )

    recommended_skills = [

        "Azure",

        "AWS",

        "SIEM",

        "Incident Response",

        "Network Security"

    ]

    score = min(

        len(
            resume_skills
        ) * 5,

        100

    )

    return {

        "headline":
        headline,

        "about":
        about,

        "skills":
        recommended_skills,

        "score":
        score

    }