import sqlite3

DB_NAME = "database.db"

# ---------- CONNECTION ----------
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# ---------- INIT DATABASE ----------
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # USERS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        is_subscribed INTEGER DEFAULT 0,
        charity TEXT DEFAULT 'None'
    )
    """)

    # SCORES TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER,
        date TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    conn.close()

# ---------- USER FUNCTIONS ----------
def create_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_user(email, password):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )
    user = cur.fetchone()
    conn.close()
    return user

def subscribe_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET is_subscribed=1 WHERE id=?",
        (user_id,)
    )
    conn.commit()
    conn.close()

# ---------- SCORE FUNCTIONS ----------
def add_score_db(user_id, score, date):
    conn = get_connection()
    cur = conn.cursor()

    # get existing scores
    cur.execute(
        "SELECT id FROM scores WHERE user_id=? ORDER BY date ASC",
        (user_id,)
    )
    scores = cur.fetchall()

    # keep only last 5
    if len(scores) >= 5:
        cur.execute("DELETE FROM scores WHERE id=?", (scores[0][0],))

    # insert new
    cur.execute(
        "INSERT INTO scores (user_id, score, date) VALUES (?, ?, ?)",
        (user_id, score, date)
    )

    conn.commit()
    conn.close()

def get_scores_db(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT score, date FROM scores WHERE user_id=? ORDER BY date DESC",
        (user_id,)
    )
    scores = cur.fetchall()
    conn.close()
    return scores