from flask import Flask, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)
DATABASE = "data/database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()

    # Tables principales
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
        CREATE TABLE IF NOT EXISTS techno (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date_add DATETIME NOT NULL,
            date_upd DATETIME NOT NULL
        )
    ''')

    # Tables de liaison
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

# ---------------- Routes Collaborator ----------------
@app.route("/collaborators", methods=["GET"])
def get_collaborators():
    conn = get_db_connection()
    collaborators = conn.execute("SELECT * FROM collaborator").fetchall()
    conn.close()
    return jsonify([dict(c) for c in collaborators])

@app.route("/collaborators", methods=["POST"])
def add_collaborator():
    data = request.get_json()
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    now = datetime.datetime.now()
    
    if not firstname or not lastname:
        return jsonify({"error": "firstname and lastname are required"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO collaborator (firstname, lastname, date_add, date_upd) VALUES (?, ?, ?, ?)",
            (firstname, lastname, now, now)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400
    conn.close()
    return jsonify({"message": f"Collaborator {firstname} {lastname} added!"}), 201

# ---------------- Routes Type ----------------
@app.route("/types", methods=["GET"])
def get_types():
    conn = get_db_connection()
    types = conn.execute("SELECT * FROM type").fetchall()
    conn.close()
    return jsonify([dict(t) for t in types])

@app.route("/types", methods=["POST"])
def add_type():
    data = request.get_json()
    name = data.get("name")
    now = datetime.datetime.now()
    
    if not name:
        return jsonify({"error": "name is required"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO type (name, date_add, date_upd) VALUES (?, ?, ?)",
            (name, now, now)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400
    conn.close()
    return jsonify({"message": f"Type {name} added!"}), 201

# ---------------- Routes Project ----------------
@app.route("/projects", methods=["GET"])
def get_projects():
    conn = get_db_connection()
    projects = conn.execute("SELECT * FROM project").fetchall()
    conn.close()
    return jsonify([dict(p) for p in projects])

@app.route("/projects", methods=["POST"])
def add_project():
    data = request.get_json()
    name = data.get("name")
    now = datetime.datetime.now()
    
    if not name:
        return jsonify({"error": "name is required"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO project (name, date_add, date_upd) VALUES (?, ?, ?)",
            (name, now, now)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400
    conn.close()
    return jsonify({"message": f"Project {name} added!"}), 201

# ---------------- Routes Techno ----------------
@app.route("/technos", methods=["GET"])
def get_technos():
    conn = get_db_connection()
    technos = conn.execute("SELECT * FROM techno").fetchall()
    conn.close()
    return jsonify([dict(t) for t in technos])

@app.route("/technos", methods=["POST"])
def add_techno():
    data = request.get_json()
    name = data.get("name")
    now = datetime.datetime.now()
    
    if not name:
        return jsonify({"error": "name is required"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO techno (name, date_add, date_upd) VALUES (?, ?, ?)",
            (name, now, now)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400
    conn.close()
    return jsonify({"message": f"Techno {name} added!"}), 201

# ---------------- Routes Liaison ----------------

# Techno ↔ Type
@app.route("/techno_type", methods=["GET"])
def get_techno_type():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM techno_type").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/techno_type", methods=["POST"])
def add_techno_type():
    data = request.get_json()
    id_techno = data.get("id_techno")
    id_type = data.get("id_type")

    if not id_techno or not id_type:
        return jsonify({"error": "id_techno and id_type are required"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO techno_type (id_techno, id_type) VALUES (?, ?)",
            (id_techno, id_type)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400
    conn.close()
    return jsonify({"message": f"Techno {id_techno} linked to Type {id_type}!"}), 201

# Techno ↔ Project
@app.route("/techno_project", methods=["GET"])
def get_techno_project():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM techno_project").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/techno_project", methods=["POST"])
def add_techno_project():
    data = request.get_json()
    id_techno = data.get("id_techno")
    id_project = data.get("id_project")

    if not id_techno or not id_project:
        return jsonify({"error": "id_techno and id_project are required"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO techno_project (id_techno, id_project) VALUES (?, ?)",
            (id_techno, id_project)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400
    conn.close()
    return jsonify({"message": f"Techno {id_techno} linked to Project {id_project}!"}), 201

# Collaborator ↔ Project
@app.route("/collaborator_project", methods=["GET"])
def get_collaborator_project():
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM collaborator_project").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/collaborator_project", methods=["POST"])
def add_collaborator_project():
    data = request.get_json()
    id_collaborator = data.get("id_collaborator")
    id_project = data.get("id_project")

    if not id_collaborator or not id_project:
        return jsonify({"error": "id_collaborator and id_project are required"}), 400

    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO collaborator_project (id_collaborator, id_project) VALUES (?, ?)",
            (id_collaborator, id_project)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        return jsonify({"error": str(e)}), 400
    conn.close()
    return jsonify({"message": f"Collaborator {id_collaborator} linked to Project {id_project}!"}), 201

# ---------------- Main ----------------
if __name__ == "__main__":
    init_db()
    app.run(debug=True)
