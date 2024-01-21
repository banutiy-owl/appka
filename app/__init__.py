from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_caching import Cache

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
cache = Cache()


def create_app():
    app = Flask(__name__,  template_folder='templates',static_folder='static')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_bank.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret_key'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    cache.init_app(app) 

    from app.models import User  

    with app.app_context():
        from app.routes.auth import auth_bp
        from app.routes.main import main_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)

        db.create_all()  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    return app
