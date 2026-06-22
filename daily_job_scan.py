import subprocess
import datetime
import sys

print(
    f"Daily Scan Started: "
    f"{datetime.datetime.now()}"
)

print(
    f"Python Executable: {sys.executable}"
)

subprocess.run(
    [sys.executable, "main.py"]
)

print(
    f"Daily Scan Completed: "
    f"{datetime.datetime.now()}"
)