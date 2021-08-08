from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()()
DB_NAME = 'DB.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Hiro"  # Cookies encrypted
    app.config(['SQLALCHEMY_DATABASE_URI']) = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from models import User, Notes

    create_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_managr.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_db(app):
    if not path.exists('website/'+DB_NAME):
        db.create_app(app=app)
        print("Created DB")
