import sqlite3

class RestaurantModel:
    def __init__(self, db_path):
        self.db_path = db_path

    def create(self, name, category=None, price_range=None, distance_category=None, 
               latitude=None, longitude=None, rating=None, address=None, 
               phone=None, opening_hours=None, is_spicy=0, is_vegetarian=0, is_fast_food=0):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO restaurants 
                   (name, category, price_range, distance_category, latitude, longitude, 
                    rating, address, phone, opening_hours, is_spicy, is_vegetarian, is_fast_food) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (name, category, price_range, distance_category, latitude, longitude,
                 rating, address, phone, opening_hours, is_spicy, is_vegetarian, is_fast_food)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM restaurants")
            return [dict(row) for row in cursor.fetchall()]

    def get_by_id(self, restaurant_id):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM restaurants WHERE id = ?", (restaurant_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def search(self, category=None, price_range=None, distance_category=None, 
               exclude_spicy=False, vegetarian_only=False, exclude_fast_food=False):
        query = "SELECT * FROM restaurants WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = ?"
            params.append(category)
        if price_range:
            query += " AND price_range = ?"
            params.append(price_range)
        if distance_category:
            query += " AND distance_category = ?"
            params.append(distance_category)
        if exclude_spicy:
            query += " AND is_spicy = 0"
        if vegetarian_only:
            query += " AND is_vegetarian = 1"
        if exclude_fast_food:
            query += " AND is_fast_food = 0"
            
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def update(self, restaurant_id, **kwargs):
        if not kwargs:
            return False
            
        updates = []
        params = []
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            params.append(value)
            
        params.append(restaurant_id)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE restaurants SET {', '.join(updates)} WHERE id = ?",
                params
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, restaurant_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM restaurants WHERE id = ?", (restaurant_id,))
            conn.commit()
            return cursor.rowcount > 0
