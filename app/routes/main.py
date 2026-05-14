from flask import Blueprint, render_template, request, flash, redirect, url_for
import random
from app.models.database import RestaurantModel

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """首頁：顯示一鍵隨機推薦的介面與極簡條件篩選"""
    return render_template('index.html')

@main_bp.route('/random', methods=['GET', 'POST'])
def random_restaurant():
    """隨機推薦一家餐廳（隨便吃什麼都好核心邏輯）"""
    if request.method == 'POST':
        # 取得前端表單傳來的篩選條件
        price_level = request.form.get('price_level')
        is_vegetarian = request.form.get('is_vegetarian')
        is_spicy = request.form.get('is_spicy')
        
        # 呼叫 Model 取得所有餐廳
        all_restaurants = RestaurantModel.get_all()
        
        if not all_restaurants:
            flash('目前系統中沒有任何餐廳資料，請先新增！', 'warning')
            return redirect(url_for('main.index'))
            
        # 將 sqlite3.Row 轉成字典以便操作
        filtered = [dict(r) for r in all_restaurants]
        
        # 基本過濾邏輯
        if price_level and price_level != 'all':
            filtered = [r for r in filtered if str(r['price_level']) == price_level]
        
        if is_vegetarian == 'on':
            filtered = [r for r in filtered if r['is_vegetarian'] == 1]
            
        if is_spicy == 'on':
            filtered = [r for r in filtered if r['is_spicy'] == 1]
            
        # 若過濾後沒有符合的餐廳，退回全部餐廳池並顯示提示
        if not filtered:
            flash('沒有完全符合條件的餐廳，幫你隨機挑選一家！', 'info')
            filtered = [dict(r) for r in all_restaurants]
            
        # 核心：隨機挑選一家
        selected_restaurant = random.choice(filtered)
        
        # 將結果傳入模板呈現
        return render_template('index.html', recommended=selected_restaurant)
        
    # 如果是 GET 請求，直接導回首頁
    return redirect(url_for('main.index'))

# 提供一個簡單的路由來手動新增測試資料，方便驗證功能
@main_bp.route('/add_test_data')
def add_test_data():
    RestaurantModel.create({'name': '麥當勞', 'type': '速食', 'price_level': 1, 'address': '台北市中正區', 'is_vegetarian': 0, 'is_spicy': 0})
    RestaurantModel.create({'name': '鼎泰豐', 'type': '中式', 'price_level': 3, 'address': '台北市信義區', 'is_vegetarian': 0, 'is_spicy': 0})
    RestaurantModel.create({'name': '果然匯', 'type': '素食', 'price_level': 2, 'address': '台北市大安區', 'is_vegetarian': 1, 'is_spicy': 0})
    RestaurantModel.create({'name': '麻神麻辣火鍋', 'type': '火鍋', 'price_level': 3, 'address': '台北市松山區', 'is_vegetarian': 0, 'is_spicy': 1})
    flash('測試餐廳資料已加入！', 'success')
    return redirect(url_for('main.index'))
