from flask import request, render_template, redirect, url_for, jsonify
from . import roulette_bp

@roulette_bp.route('/create', methods=['POST'])
def create_room():
    """
    建立新的多人決策輪盤房間。
    輸入：建立者 ID（若已登入）。
    處理邏輯：
        1. 產生一組 UUID。
        2. 新增一筆紀錄到 ROOM 表，狀態設為 open。
    輸出：重導向至 /room/<room_id>。
    """
    pass

@roulette_bp.route('/<room_id>', methods=['GET'])
def view_room(room_id):
    """
    進入特定的輪盤房間頁面。
    輸入：URL 參數 room_id。
    處理邏輯：
        1. 確認房間是否存在。
        2. 取得該房間的所有 PROPOSAL（提議）紀錄。
    輸出：渲染 roulette.html 模板。
    """
    pass

@roulette_bp.route('/<room_id>/propose', methods=['POST'])
def propose(room_id):
    """
    參與者在房間內提交想吃的選項。
    輸入：表單資料 user_name、restaurant_name 或 restaurant_id。
    處理邏輯：
        1. 驗證房間是否仍在開放中。
        2. 新增紀錄到 PROPOSAL 表。
    輸出：重導向回 /room/<room_id> 刷新畫面。
    """
    pass

@roulette_bp.route('/<room_id>/spin', methods=['POST'])
def spin(room_id):
    """
    啟動輪盤抽選，系統隨機選出結果並更新房間狀態。
    輸入：URL 參數 room_id。
    處理邏輯：
        1. 檢查觸發權限。
        2. 從 PROPOSAL 清單中隨機抽選出一個結果。
        3. 更新 ROOM 表狀態為 closed，記錄 result_id。
    輸出：回傳 JSON 給前端以便播放動畫並顯示最終結果。
    """
    pass
