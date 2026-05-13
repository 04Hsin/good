import sqlite3
from datetime import datetime

class HistoryModel:
    def __init__(self, db_path):
        self.db_path = db_path

    # Favorite Methods
    def add_favorite(self, user_id, restaurant_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO favorites (user_id, restaurant_id) VALUES (?, ?)",
                    (user_id, restaurant_id)
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def get_favorites(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT r.*, f.created_at as favorited_at 
                   FROM restaurants r 
                   JOIN favorites f ON r.id = f.restaurant_id 
                   WHERE f.user_id = ?""",
                (user_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def remove_favorite(self, user_id, restaurant_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM favorites WHERE user_id = ? AND restaurant_id = ?",
                (user_id, restaurant_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    # Blacklist Methods
    def add_to_blacklist(self, user_id, restaurant_id, type='temporary', expires_at=None):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO blacklists (user_id, restaurant_id, type, expires_at) VALUES (?, ?, ?, ?)",
                    (user_id, restaurant_id, type, expires_at)
                )
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def get_blacklist(self, user_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT r.*, b.type, b.expires_at 
                   FROM restaurants r 
                   JOIN blacklists b ON r.id = b.restaurant_id 
                   WHERE b.user_id = ?""",
                (user_id,)
            )
            return [dict(row) for row in cursor.fetchall()]

    def remove_from_blacklist(self, user_id, restaurant_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM blacklists WHERE user_id = ? AND restaurant_id = ?",
                (user_id, restaurant_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    # Search History Methods
    def add_search_history(self, user_id, restaurant_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO search_history (user_id, restaurant_id) VALUES (?, ?)",
                (user_id, restaurant_id)
            )
            conn.commit()
            return cursor.lastrowid

    def get_search_history(self, user_id, limit=20):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                """SELECT r.*, s.created_at as searched_at 
                   FROM restaurants r 
                   JOIN search_history s ON r.id = s.restaurant_id 
                   WHERE s.user_id = ? 
                   ORDER BY s.created_at DESC LIMIT ?""",
                (user_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
