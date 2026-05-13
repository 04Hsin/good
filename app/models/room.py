import sqlite3

class RoomModel:
    def __init__(self, db_path):
        self.db_path = db_path

    # Room Methods
    def create_room(self, room_id, creator_id=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO rooms (id, creator_id) VALUES (?, ?)",
                (room_id, creator_id)
            )
            conn.commit()
            return room_id

    def get_room(self, room_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM rooms WHERE id = ?", (room_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_room_status(self, room_id, status, result_id=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if result_id:
                cursor.execute(
                    "UPDATE rooms SET status = ?, result_id = ? WHERE id = ?",
                    (status, result_id, room_id)
                )
            else:
                cursor.execute(
                    "UPDATE rooms SET status = ? WHERE id = ?",
                    (status, room_id)
                )
            conn.commit()
            return cursor.rowcount > 0

    def delete_room(self, room_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM rooms WHERE id = ?", (room_id,))
            conn.commit()
            return cursor.rowcount > 0

    # Proposal Methods
    def add_proposal(self, room_id, user_name, restaurant_name, restaurant_id=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO proposals (room_id, user_name, restaurant_name, restaurant_id) 
                   VALUES (?, ?, ?, ?)""",
                (room_id, user_name, restaurant_name, restaurant_id)
            )
            conn.commit()
            return cursor.lastrowid

    def get_proposals(self, room_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM proposals WHERE room_id = ?", (room_id,))
            return [dict(row) for row in cursor.fetchall()]

    def delete_proposal(self, proposal_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM proposals WHERE id = ?", (proposal_id,))
            conn.commit()
            return cursor.rowcount > 0
