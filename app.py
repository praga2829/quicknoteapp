from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = sqlite3.connect("notes.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create database table
def create_table():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Display homepage
@app.route("/")
def home():
    return render_template("index.html")


# Save note
@app.route("/save", methods=["POST"])
def save_note():

    data = request.get_json()

    note = data.get("content", "").strip()

    if not note:
        return jsonify({"message": "Note cannot be empty"}), 400

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO notes (content) VALUES (?)",
        (note,)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Note saved successfully!"})


# Get all notes
@app.route("/notes", methods=["GET"])
def get_notes():

    conn = get_db_connection()

    notes = conn.execute(
        "SELECT * FROM notes ORDER BY id DESC"
    ).fetchall()

    conn.close()

    return jsonify([
        {
            "id": note["id"],
            "content": note["content"]
        }
        for note in notes
    ])


if __name__ == "__main__":
    create_table()
    app.run(debug=True)