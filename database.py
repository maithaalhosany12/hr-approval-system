import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    # Main Requests Table
    c.execute('''CREATE TABLE IF NOT EXISTS requests
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  number TEXT, unit TEXT, name TEXT, appt_date TEXT,
                  subject TEXT, submit_date TIMESTAMP, status TEXT,
                  stage INTEGER DEFAULT 1,
                  attachment_path TEXT)''')
    
    # Approvals Table (Tracks time and decisions)
    c.execute('''CREATE TABLE IF NOT EXISTS approvals
                 (request_id INTEGER, stage_name TEXT, actor_name TEXT, 
                  decision TEXT, comments TEXT, processed_at TIMESTAMP,
                  duration_hours REAL)''')

    # Appeals Table
    c.execute('''CREATE TABLE IF NOT EXISTS appeals
                 (request_id INTEGER, appeal_count INTEGER, appeal_date TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_appeal_count(request_id):
    conn = sqlite3.connect('requests.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM appeals WHERE request_id = ?", (request_id,))
    count = c.fetchone()[0]
    conn.close()
    return count
