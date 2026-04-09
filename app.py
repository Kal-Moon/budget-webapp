from flask import Flask, render_template, request, redirect, url_for

records = []

import sqlite3

def init_db():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
                   id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    memo    TEXT,
                   amount   INTEGER,
                   type TEXT,
                    category    TEXT,
                   date     TEXT
                   )
                   """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS categories(
                   id   INTEGER PRIMARY KEY,
                   name TEXT)
                   """)
    
    cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (1, '식비')")
    cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (2, '교통/차량')")
    cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (3, '패션/미용')")
    cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (4, '주거/통신')")
    cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (5, '건강')")
    cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (6, '교육')")
    cursor.execute("INSERT OR IGNORE INTO categories (id, name) VALUES (7, '생활용품')")
    
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)

@app.route("/")
def home():
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records")
    records = cursor.fetchall()
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()

    conn.close()

    income =0 
    expense = 0
    for record in records:
        if record[3] == "income":
            income += record[2]
        elif record[3] == "expense":
            expense += record[2]
    total = income - expense

    return render_template("index.html", records=records, categories=categories,
                           income=income, expense=expense, total=total)

@app.route("/about")
def introduce():
    return "자기소개"

@app.route("/stats")
def stats():
    return render_template("stats.html")    

@app.route("/settings")
def settings():
    return render_template("settings.html")  

@app.route("/calendar")
def calendar():
    return render_template("calendar.html")

@app.route("/monthly")
def monthly():
    return render_template("monthly.html")

@app.route("/memo")
def memo():
    return render_template("memo.html")

@app.route("/add", methods=["POST"])
def add():
    memo_text = request.form["memo"]
    amount = request.form["amount"]
    type_value = request.form["type"]
    category_id = request.form["category"]
  
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO records (memo, amount, type, category) VALUES (?, ?, ?, ?)",
                   (memo_text, amount, type_value, category_id))
    conn.commit()
    conn.close()

    return redirect(url_for("home"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM records WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

@app.route("/edit/<int:id>")
def edit(id):
    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records WHERE id =?", (id,))
    record = cursor.fetchone()
    conn.close()
    return render_template("edit.html", record=record)

@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    memo_text = request.form["memo"]
    amount = request.form["amount"]
    type_value = request.form["type"]

    conn = sqlite3.connect("budget.db")
    cursor = conn.cursor()
    cursor.execute("""
                   UPDATE records
                   SET memo=?, amount=?, type=?
                   WHERE id=?
                   """, (memo_text, amount, type_value, id))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)