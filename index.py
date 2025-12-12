from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import datetime

app = Flask(__name__)
CORS(app)
DATABASE = "data/database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS collaborator (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            date_add DATETIME NOT NULL,
            date_upd DATETIME NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_add DATETIME NOT NULL,
            date_upd DATETIME NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS project (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_add DATETIME NOT NULL,
            date_upd DATETIME NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS Techno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_add DATETIME NOT NULL,
            date_upd DATETIME NOT NULL
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS techno_type (
            id_techno INTEGER,
            id_type INTEGER,
            PRIMARY KEY(id_techno, id_type) 
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS techno_project (
            id_techno INTEGER,
            id_project INTEGER,
            PRIMARY KEY(id_techno, id_project)  
        )
    ''')

    conn.execute('''
        CREATE TABLE IF NOT EXISTS collaborator_project (
            id_collaborator INTEGER,
            id_project INTEGER,
            PRIMARY KEY(id_collaborator, id_project)  

        )
    ''')
    conn.commit()
    conn.close()

@app.route("/collaborators", methods=["GET"])
def get_users():
    conn = get_db_connection()
    collaborators = conn.execute("SELECT * FROM collaborator").fetchall()
    conn.close()
    return jsonify([dict(c) for c in collaborators])

@app.route("/collaborators", methods=["POST"])
def add_user():
    data = request.get_json()
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    date_add = datetime.datetime.now()
    date_upd = datetime.datetime.now()
    
    if not firstname or not lastname:
        return jsonify({"error": "firstname and lastname are required"}), 400

    conn = get_db_connection()
    conn.execute("INSERT INTO collaborator (firstname, lastname, date_add, date_upd) VALUES (?, ?, ?, ?)", (firstname, lastname, date_add, date_upd))
    conn.commit()

    conn.close()
    return jsonify({"message": f"Collaborators {firstname} {lastname} added!"}), 201

if __name__ == "__main__":
        init_db()
        app.run(debug=True)
