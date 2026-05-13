-- 隨便吃什麼都好系統 (Whatever Eatery) - SQLite Schema

-- 使用者
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 餐廳
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT,
    price_range TEXT, -- $, $$, $$$
    distance_category TEXT, -- 5min, 10min, transport
    latitude REAL,
    longitude REAL,
    rating REAL,
    address TEXT,
    phone TEXT,
    opening_hours TEXT,
    is_spicy INTEGER DEFAULT 0, -- 0: False, 1: True
    is_vegetarian INTEGER DEFAULT 0,
    is_fast_food INTEGER DEFAULT 0
);

-- 我的最愛
CREATE TABLE IF NOT EXISTS favorites (
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, restaurant_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
);

-- 黑名單 (暫時或永久)
CREATE TABLE IF NOT EXISTS blacklists (
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,
    type TEXT DEFAULT 'temporary', -- 'temporary' or 'permanent'
    expires_at DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, restaurant_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE
);

-- 搜尋歷史
CREATE TABLE IF NOT EXISTS search_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    restaurant_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE SET NULL
);

-- 輪盤房間
CREATE TABLE IF NOT EXISTS rooms (
    id TEXT PRIMARY KEY, -- Random string / UUID
    creator_id INTEGER,
    status TEXT DEFAULT 'open', -- 'open' or 'closed'
    result_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (result_id) REFERENCES restaurants(id) ON DELETE SET NULL
);

-- 房間提議
CREATE TABLE IF NOT EXISTS proposals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id TEXT NOT NULL,
    user_name TEXT,
    restaurant_name TEXT,
    restaurant_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE SET NULL
);
