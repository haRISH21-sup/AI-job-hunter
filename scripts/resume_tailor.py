def generate_prompt(resume_text, job_description):

    prompt = f"""
You are an ATS Resume Expert.

TASK:
Rewrite the resume so it better matches the Job Description.

RULES:
- Do not invent experience.
- Keep all information truthful.
- Improve ATS keywords.
- Highlight relevant skills.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}
"""

    return prompt