from datetime import datetime


def get_followup_jobs(
        applications
):

    reminders = []

    today = datetime.now()

    for _, row in applications.iterrows():

        try:

            if (
                row["status"]
                == "Applied"
            ):

                applied_date = (
                    datetime.strptime(
                        row[
                            "date_applied"
                        ],
                        "%Y-%m-%d"
                    )
                )

                days = (
                    today
                    -
                    applied_date
                ).days

                if days >= 7:

                    reminders.append({

                        "company":
                        row["company"],

                        "job_title":
                        row["job_title"],

                        "days":
                        days

                    })

        except Exception:

            pass

    return reminders