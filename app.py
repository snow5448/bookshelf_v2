from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("books.db")

#起動時にテーブルを作る
db = get_db()
db.execute("""CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            title TEXT NOT NULL UNIQUE)""")
db.execute("""CREATE TABLE IF NOT EXISTS volumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            series_id INTEGER NOT NULL REFERENCES series(id), 
            number INTEGER NOT NULL, 
            UNIQUE(series_id, number))""")
db.close()

@app.route("/", methods=["GET", "POST"])
def index():
    db = get_db()
    if request.method == "POST":
        title = request.form["title"]
        db.execute("INSERT OR IGNORE INTO series (title) VALUES (?)", (title,))
        db.commit()
        db.close()
        return redirect(url_for("index"))

    rows = db.execute("SELECT id, title FROM series").fetchall()
    db.close()
    return render_template("index.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)