from flask import Blueprint

# 初始化各個 Blueprint
main_bp = Blueprint('main', __name__)
user_bp = Blueprint('user', __name__)
roulette_bp = Blueprint('roulette', __name__, url_prefix='/room')

# 將所有的 blueprint 集中，方便在 app.py 中一次註冊
def register_blueprints(app):
    from .main import main_bp
    from .user import user_bp
    from .roulette import roulette_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(roulette_bp)
