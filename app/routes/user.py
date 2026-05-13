from flask import request, render_template, redirect, url_for
from . import user_bp

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    會員登入。
    處理邏輯：顯示登入表單或接收帳密進行驗證。
    """
    pass

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    會員註冊。
    處理邏輯：顯示註冊表單或接收帳密寫入 USER 表。
    """
    pass

@user_bp.route('/logout', methods=['GET'])
def logout():
    """
    會員登出。
    處理邏輯：清除 Session。
    輸出：重導向回首頁。
    """
    pass

@user_bp.route('/profile', methods=['GET'])
def profile():
    """
    查看使用者的歷史推薦紀錄與我的最愛清單。
    處理邏輯：
        1. 驗證是否登入。
        2. 查詢 SEARCH_HISTORY 與 FAVORITE。
    輸出：渲染 profile.html。
    """
    pass

@user_bp.route('/blacklist', methods=['POST'])
def add_blacklist():
    """
    將不滿意的餐廳短暫加入黑名單，並自動重新觸發推薦。
    輸入：restaurant_id。
    處理邏輯：
        1. 寫入 BLACKLIST 表（暫時排除）。
        2. 自動重抽餐廳。
    輸出：重導向回首頁，或重新回傳推薦結果。
    """
    pass

@user_bp.route('/favorite', methods=['POST'])
def add_favorite():
    """
    將滿意的餐廳加入個人的最愛清單。
    輸入：restaurant_id。
    處理邏輯：
        1. 確認是否登入。
        2. 寫入 FAVORITE 表。
    輸出：重導向回上一頁或個人檔案頁。
    """
    pass
