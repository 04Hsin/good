import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
    
    # 註冊 Blueprints
    from app.routes.main import main_bp
    from app.routes.roulette import roulette_bp
    from app.routes.user import user_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(roulette_bp)
    app.register_blueprint(user_bp)
    
    return app
