import sqlite3

def create_connection():
    return sqlite3.connect("resumes.db")

def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        score REAL
    )
    """)

    conn.commit()
    conn.close()

def insert_candidate(name, email, phone, skills, score):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates (name, email, phone, skills, score)
    VALUES (?, ?, ?, ?, ?)
    """, (name, email, phone, skills, score))

    conn.commit()
    conn.close()

def get_all_candidates():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM candidates ORDER BY score DESC")
    data = cursor.fetchall()

    conn.close()
    return data