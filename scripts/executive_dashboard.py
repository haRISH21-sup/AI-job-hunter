def generate_executive_summary(
        readiness_score,
        salary_info,
        missing_skills
):

    if readiness_score >= 80:

        status = (
            "Highly Competitive"
        )

    elif readiness_score >= 60:

        status = (
            "Moderately Competitive"
        )

    else:

        status = (
            "Needs Improvement"
        )

    summary = f"""

Career Status:
{status}

Interview Readiness:
{readiness_score}%

Recommended Role:
{salary_info['recommended_role']}

Expected Salary:
{salary_info['salary_range']}

Top Missing Skills:
{', '.join(missing_skills[:5])}

"""

    return summary