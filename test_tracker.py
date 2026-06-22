from scripts.application_tracker import (
    add_application,
    view_applications,
    update_status
)

from scripts.application_dashboard import (
    show_dashboard
)

from scripts.export_applications import (
    export_applications_to_excel
)

add_application(
    "Eventus Security",
    "Security Analyst"
)

add_application(
    "H&R Block India",
    "Security Engineer"
)

update_status(
    "H&R Block India",
    "Security Engineer",
    "Interview"
)

view_applications()

show_dashboard()

export_applications_to_excel()