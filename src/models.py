import datetime
from src.config import get_db_connection

class BaseModel:
    def __init__(self, table_name):
        self.table_name = table_name

    def get_all(self):
        conn = get_db_connection()
        items = conn.execute(f"SELECT * FROM {self.table_name}").fetchall()
        conn.close()
        return [dict(item) for item in items]

    def get_by_id(self, item_id):
        conn = get_db_connection()
        item = conn.execute(f"SELECT * FROM {self.table_name} WHERE id = ?", (item_id,)).fetchone()
        conn.close()
        return dict(item) if item else None

    def create(self, data):
        now = datetime.datetime.now()
        data['date_add'] = now
        data['date_upd'] = now

        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        values = tuple(data.values())

        conn = get_db_connection()
        cursor = conn.execute(
            f"INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})",
            values
        )
        conn.commit()
        item_id = cursor.lastrowid
        conn.close()
        return item_id

    def update(self, item_id, data):
        data['date_upd'] = datetime.datetime.now()

        set_clause = ', '.join([f"{key} = ?" for key in data.keys()])
        values = tuple(data.values()) + (item_id,)

        conn = get_db_connection()
        conn.execute(
            f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?",
            values
        )
        conn.commit()
        affected_rows = conn.total_changes
        conn.close()
        return affected_rows > 0

    def delete(self, item_id):
        conn = get_db_connection()
        conn.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (item_id,))
        conn.commit()
        affected_rows = conn.total_changes
        conn.close()
        return affected_rows > 0


class RelationModel:
    def __init__(self, table_name, field1, field2):
        self.table_name = table_name
        self.field1 = field1
        self.field2 = field2

    def get_all(self):
        conn = get_db_connection()
        items = conn.execute(f"SELECT * FROM {self.table_name}").fetchall()
        conn.close()
        return [dict(item) for item in items]

    def create(self, data):
        conn = get_db_connection()
        cursor = conn.execute(
            f"INSERT INTO {self.table_name} ({self.field1}, {self.field2}) VALUES (?, ?)",
            (data[self.field1], data[self.field2])
        )
        conn.commit()
        conn.close()
        return True

    def delete(self, value1, value2):
        conn = get_db_connection()
        conn.execute(
            f"DELETE FROM {self.table_name} WHERE {self.field1} = ? AND {self.field2} = ?",
            (value1, value2)
        )
        conn.commit()
        affected_rows = conn.total_changes
        conn.close()
        return affected_rows > 0


collaborator_model = BaseModel('collaborator')
type_model = BaseModel('type')
project_model = BaseModel('project')
techno_model = BaseModel('techno')

techno_type_model = RelationModel('techno_type', 'id_techno', 'id_type')
techno_project_model = RelationModel('techno_project', 'id_techno', 'id_project')
collaborator_project_model = RelationModel('collaborator_project', 'id_collaborator', 'id_project')
