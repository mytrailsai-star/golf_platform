from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import random
from datetime import datetime

from db import (
    init_db,
    create_user,
    get_user,
    subscribe_user,
    add_score_db,
    get_scores_db
)

app = Flask(__name__)
CORS(app)

# ---------- DATABASE ----------
def get_connection():
    return sqlite3.connect("database.db", check_same_thread=False)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT,
        password TEXT,
        is_subscribed INTEGER DEFAULT 0,
        charity TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------- ROUTES ----------

@app.route("/")
def home():
    return "Backend is running ✅"

# SIGNUP
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                (data["email"], data["password"]))
    conn.commit()
    conn.close()

    return jsonify({"message": "User created"})

# LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE email=? AND password=?",
                (data["email"], data["password"]))
    user = cur.fetchone()
    conn.close()

    if user:
        return jsonify({"user_id": user[0]})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# SUBSCRIBE
@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("UPDATE users SET is_subscribed=1 WHERE id=?",
                (data["user_id"],))
    conn.commit()
    conn.close()

    return jsonify({"message": "Subscribed"})

# ADD SCORE (ONLY 5 LATEST)
@app.route("/add_score", methods=["POST"])
def add_score():
    data = request.json
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM scores WHERE user_id=? ORDER BY date ASC",
                (data["user_id"],))
    scores = cur.fetchall()

    if len(scores) >= 5:
        cur.execute("DELETE FROM scores WHERE id=?", (scores[0][0],))

    cur.execute(
        "INSERT INTO scores (user_id, score, date) VALUES (?, ?, ?)",
        (data["user_id"], data["score"], datetime.now().strftime("%Y-%m-%d"))
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Score added"})

# GET SCORES
@app.route("/scores/<int:user_id>")
def get_scores(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT score, date FROM scores WHERE user_id=? ORDER BY date DESC",
                (user_id,))
    data = cur.fetchall()
    conn.close()

    return jsonify(data)

# DRAW
@app.route("/draw")
def draw():
    numbers = random.sample(range(1, 46), 5)
    return jsonify(numbers)

# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)