import imp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    """ Creates the app instance """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "NWBFBEFWBFWJEBFHWJ"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix="/")   # urlprefix is the 'proxy' or 'starter' only
    app.register_blueprint(auth, url_prefix="/")

    from .models import User
    create_database(app)

    loginmanager = LoginManager()
    loginmanager.login_view = "auth.login"
    loginmanager.init_app(app)

    @loginmanager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("dashboard/" + DB_NAME):
        db.create_all(app = app)
        print("Database created")
