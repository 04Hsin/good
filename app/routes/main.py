from flask import request, render_template, redirect, url_for
from . import main_bp

@main_bp.route('/', methods=['GET'])
def index():
    """
    顯示首頁，包含一鍵隨機推薦表單與極簡篩選條件。
    處理邏輯：
        1. 檢查使用者登入狀態。
        2. 渲染 index.html 顯示極簡條件篩選表單。
    """
    pass

@main_bp.route('/recommend', methods=['POST'])
def recommend():
    """
    接收篩選條件與定位，查詢資料庫並回傳隨機推薦的餐廳。
    輸入：距離範圍、價格區間、排除條件標籤、地理位置經緯度。
    處理邏輯：
        1. 解析表單與位置資料。
        2. 從 RESTAURANT 表篩選符合條件且不在使用者 BLACKLIST 的餐廳。
        3. 隨機抽選一家。
        4. 若登入，寫入 SEARCH_HISTORY。
    輸出：渲染 index.html 並將結果傳給前端觸發動畫。
    """
    pass
