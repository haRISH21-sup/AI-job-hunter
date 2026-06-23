def get_salary_insights(
        readiness_score
):

    if readiness_score >= 85:

        return {

            "current_role":
            "Network Engineer",

            "recommended_role":
            "Network Security Engineer",

            "salary_range":
            "₹8 LPA - ₹12 LPA",

            "next_role":
            "SOC Analyst",

            "next_salary":
            "₹12 LPA - ₹18 LPA"
        }

    elif readiness_score >= 70:

        return {

            "current_role":
            "Network Engineer",

            "recommended_role":
            "Network Engineer",

            "salary_range":
            "₹5 LPA - ₹8 LPA",

            "next_role":
            "Network Security Engineer",

            "next_salary":
            "₹8 LPA - ₹12 LPA"
        }

    else:

        return {

            "current_role":
            "Junior Network Engineer",

            "recommended_role":
            "Network Engineer",

            "salary_range":
            "₹3 LPA - ₹6 LPA",

            "next_role":
            "Network Security Engineer",

            "next_salary":
            "₹8 LPA - ₹12 LPA"
        }