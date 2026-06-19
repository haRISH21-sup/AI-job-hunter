import pandas as pd

def collect_jobs():
    jobs = pd.read_csv("data/sample_jobs.csv")
    return jobs