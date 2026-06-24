import sqlite3
import os

DB_PATH = "database/jobhunter.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def initialize_database():

    os.makedirs("database", exist_ok=True)

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================
    # APPLICATIONS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        company TEXT NOT NULL,
        job_title TEXT NOT NULL,
        date_applied TEXT,
        status TEXT,
        notes TEXT,
        UNIQUE(user_id, company, job_title)
    )
    """)

    # =====================================
    # JOBS TABLE
    # =====================================

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

    # =====================================
    # JOB HISTORY TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scan_date TEXT,
        job_title TEXT,
        company TEXT,
        location TEXT,
        match_score REAL
    )
    """)

    # =====================================
    # SAVED JOBS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        job_title TEXT,
        company TEXT,
        location TEXT,
        match_score REAL,
        apply_url TEXT,
        saved_date TEXT
    )
    """)

    # =====================================
    # WATCHLIST TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS watchlist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        company TEXT
    )
    """)

    # =====================================
    # RECRUITERS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recruiters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        recruiter_name TEXT,
        company TEXT,
        email TEXT,
        linkedin TEXT,
        status TEXT,
        notes TEXT,
        last_contact TEXT
    )
    """)

    # =====================================
    # USERS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    conn.commit()
    conn.close()


initialize_database()