import sqlite3
from datetime import datetime

DB_FILE = "cards.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            uid TEXT UNIQUE NOT NULL,
            role TEXT DEFAULT 'user',
            added_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_card(uid, role="user"):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO cards (uid, role, added_at) VALUES (?, ?, ?)",
                  (uid, role, datetime.now().isoformat()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def remove_card(uid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM cards WHERE uid = ?", (uid,))
    conn.commit()
    conn.close()

def list_cards():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, uid, role, added_at FROM cards")
    rows = c.fetchall()
    conn.close()
    return rows

def is_authorized(uid):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT role FROM cards WHERE uid = ?", (uid,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None
