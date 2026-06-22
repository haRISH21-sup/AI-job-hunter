import sqlite3
import os

DB_PATH = "database/jobhunter.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():

    os.makedirs("database", exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        company TEXT NOT NULL,

        job_title TEXT NOT NULL,

        date_applied TEXT,

        status TEXT,

        notes TEXT,

        UNIQUE(company, job_title)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        job_title TEXT,

        company TEXT,

        location TEXT,

        description TEXT,

        match_score REAL,

        apply_url TEXT
    )
    """)

    conn.commit()
    conn.close()