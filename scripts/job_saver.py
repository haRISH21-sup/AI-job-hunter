import pandas as pd
import os

def save_job(job):

    file_path = "data/jobs/jobs.csv"

    df = pd.read_csv(file_path)

    df.loc[len(df)] = job

    df.to_csv(file_path, index=False)

    print("Job Saved")