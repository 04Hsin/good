from flask import Blueprint, render_template

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/profile')
def profile():
    """使用者個人歷史紀錄與收藏介面"""
    return render_template('profile.html')
