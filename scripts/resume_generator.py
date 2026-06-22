from fpdf import FPDF


def generate_resume(
    job_title,
    company,
    skills
):

    pdf = FPDF()

    pdf.add_page()

    pdf.set_font("Arial", size=12)

    pdf.cell(
        200,
        10,
        txt="Hari Prasad MR",
        ln=True
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

    pdf.ln(10)

    pdf.multi_cell(
        0,
        10,
        txt=
        "Network Engineer with hands-on experience in "
        "network monitoring, SIEM monitoring, Linux, "
        "OPNsense Firewall, Wireshark, Nmap, "
        "Kaspersky KUMA SIEM, DNS, DHCP, "
        "Routing, Switching and Cyber Security."
    )

    pdf.ln(5)

    pdf.multi_cell(
        0,
        10,
        txt=f"Relevant Skills: {skills}"
    )

    filename = (
        f"generated_resumes/"
        f"{company}_{job_title}.pdf"
    )

    filename = filename.replace("/", "_")

    pdf.output(filename)

    print(
        f"Resume Generated: {filename}"
    )