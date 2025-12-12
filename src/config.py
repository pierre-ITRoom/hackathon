import sqlite3

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
