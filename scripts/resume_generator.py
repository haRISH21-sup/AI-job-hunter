from fpdf import FPDF


def generate_resume(
    job_title,
    company,
    summary,
    skills
):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font(
        "Arial",
        "B",
        16
    )

    pdf.cell(
        200,
        10,
        txt="Hari Prasad MR",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        12
    )

    pdf.cell(
        200,
        10,
        txt=f"Target Role: {job_title}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        txt=f"Company: {company}",
        ln=True
    )

    pdf.ln(5)

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        txt="Professional Summary",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.multi_cell(
        0,
        8,
        summary
    )

    pdf.ln(5)

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        txt="Relevant Skills",
        ln=True
    )

    pdf.set_font(
        "Arial",
        "",
        11
    )

    pdf.multi_cell(
    0,
    8,
    ", ".join(skills)
    )

    filename = (
        f"generated_resumes/"
        f"{company}_{job_title}.pdf"
    )

    filename = (
        filename
        .replace("/", "_")
        .replace("\\", "_")
    )

    pdf.output(filename)

    print(
        f"Resume Generated: {filename}"
    )