from flask import Blueprint, render_template

roulette_bp = Blueprint('roulette', __name__, url_prefix='/roulette')

@roulette_bp.route('/')
def index():
    """多人決策輪盤首頁"""
    return render_template('roulette.html')
