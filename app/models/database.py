import sqlite3
import os

# 設定 database.db 的路徑 (專案根目錄/instance/database.db)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
DATABASE_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """
    取得資料庫連線
    回傳：sqlite3.Connection 物件
    """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

class RestaurantModel:
    """餐廳資料 Model"""
    
    @staticmethod
    def create(data):
        """
        新增一筆餐廳記錄
        :param data: 包含 name, type, price_level, address, is_vegetarian, is_spicy 的字典
        """
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO restaurants (name, type, price_level, address, is_vegetarian, is_spicy) VALUES (?, ?, ?, ?, ?, ?)',
                (
                    data.get('name'), 
                    data.get('type'), 
                    data.get('price_level'), 
                    data.get('address'), 
                    data.get('is_vegetarian', 0), 
                    data.get('is_spicy', 0)
                )
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating restaurant: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有餐廳記錄"""
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM restaurants').fetchall()
        except sqlite3.Error as e:
            print(f"Error getting restaurants: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id):
        """取得單筆餐廳記錄"""
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM restaurants WHERE id = ?', (id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Error getting restaurant {id}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(id, data):
        """
        更新餐廳記錄
        :param id: 餐廳 ID
        :param data: 欲更新的資料字典
        """
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE restaurants SET name=?, type=?, price_level=?, address=?, is_vegetarian=?, is_spicy=? WHERE id=?',
                (
                    data.get('name'), 
                    data.get('type'), 
                    data.get('price_level'), 
                    data.get('address'), 
                    data.get('is_vegetarian', 0), 
                    data.get('is_spicy', 0), 
                    id
                )
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating restaurant {id}: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(id):
        """刪除餐廳記錄"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM restaurants WHERE id = ?', (id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting restaurant {id}: {e}")
            return False
        finally:
            conn.close()


class RoomModel:
    """多人決策房間 Model"""
    
    @staticmethod
    def create(data):
        """新增一筆房間記錄"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO rooms (room_code, status) VALUES (?, ?)',
                (data.get('room_code'), data.get('status', 'active'))
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating room: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有房間記錄"""
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM rooms').fetchall()
        except sqlite3.Error as e:
            print(f"Error getting rooms: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id):
        """取得單筆房間記錄"""
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM rooms WHERE id = ?', (id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Error getting room {id}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_by_code(room_code):
        """以 room_code 取得單筆房間記錄"""
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM rooms WHERE room_code = ?', (room_code,)).fetchone()
        except sqlite3.Error as e:
            print(f"Error getting room code {room_code}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(id, data):
        """更新房間記錄"""
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE rooms SET status=? WHERE id=?',
                (data.get('status'), id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating room {id}: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(id):
        """刪除房間記錄"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM rooms WHERE id = ?', (id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting room {id}: {e}")
            return False
        finally:
            conn.close()


class UserModel:
    """使用者 Model"""
    
    @staticmethod
    def create(data):
        """新增一筆使用者記錄"""
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, preferences) VALUES (?, ?)',
                (data.get('username'), data.get('preferences', '{}'))
            )
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """取得所有使用者記錄"""
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM users').fetchall()
        except sqlite3.Error as e:
            print(f"Error getting users: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(id):
        """取得單筆使用者記錄"""
        conn = get_db_connection()
        try:
            return conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
        except sqlite3.Error as e:
            print(f"Error getting user {id}: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def update(id, data):
        """更新使用者記錄"""
        conn = get_db_connection()
        try:
            conn.execute(
                'UPDATE users SET username=?, preferences=? WHERE id=?',
                (data.get('username'), data.get('preferences'), id)
            )
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating user {id}: {e}")
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(id):
        """刪除使用者記錄"""
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM users WHERE id = ?', (id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting user {id}: {e}")
            return False
        finally:
            conn.close()

def init_db(app):
    """初始化資料庫 (透過 schema.sql)"""
    with app.app_context():
        conn = get_db_connection()
        schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()

