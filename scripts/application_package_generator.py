import os
import shutil


def create_application_package(
        company,
        job_title
):

    folder_name = (
        f"application_packages/"
        f"{company}_{job_title}"
    )

    folder_name = (
        folder_name
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
    )

    os.makedirs(
        folder_name,
        exist_ok=True
    )

    files_to_copy = [

        (
            f"generated_docx_resumes/"
            f"{company}_{job_title}.docx"
        ),

        (
            f"generated_docx_cover_letters/"
            f"{company}_{job_title}.docx"
        ),

        (
            f"interview_prep/"
            f"{company}_{job_title}_Questions.docx"
        ),

        (
            f"interview_answers/"
            f"{company}_{job_title}_Answers.docx"
        ),

        (
            f"skill_gap_reports/"
            f"{company}_{job_title}_SkillGap.docx"
        ),

        (
            f"ats_reports/"
            f"{company}_{job_title}_ATS_Report.docx"
        )

    ]

    for file_path in files_to_copy:

        if os.path.exists(
            file_path
        ):

            shutil.copy(
                file_path,
                folder_name
            )

    print(
        f"Application Package Created: "
        f"{folder_name}"
    )