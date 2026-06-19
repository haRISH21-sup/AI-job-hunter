import os

folders = [
    "database",
    "company_sources",
    "data",
    "jobs",
    "logs",
    "resumes",
    "generated_resumes",
    "scripts"
]

files = {
    "data/applications.csv": "company,job_title,date_applied,status,notes\n",
    "data/jobs.csv": "job_title,company,location,link,match_score,status\n",
    "data/sample_jobs.csv": """job_title,company,location,description
SOC Analyst,ABC Security,Bengaluru,"SIEM Linux Networking Firewall SOC"
Network Engineer,XYZ Networks,Chennai,"Routing Switching TCP/IP DNS DHCP"
System Administrator,Tech Corp,Hyderabad,"Windows Linux Active Directory VMware"
""",
    "database/.gitkeep": "",
    "logs/.gitkeep": "",
    "company_sources/__init__.py": "",
    "scripts/__init__.py": ""
}

print("Creating folders...")

for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"✓ {folder}")

print("\nCreating files...")

for filepath, content in files.items():

    if not os.path.exists(filepath):

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✓ {filepath}")

    else:
        print(f"Already Exists: {filepath}")

print("\nProject setup completed successfully!")