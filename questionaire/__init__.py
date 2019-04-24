import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

# from config import Config
from tools import ConfigManager


db = SQLAlchemy()
bcrypt = Bcrypt()
loginmanager = LoginManager()
loginmanager.login_view = 'users.login'
loginmanager.login_message_category = 'info'

mail = Mail()


# def app_config(app):
#     app.config['SECRET_KEY'] = 'd31b4f37bf2b1a8be9f93107c1d27ad083e92b4ed6416866b5487be73765a2b5'
#
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#
#     app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
#     app.config['MAIL_PORT'] = '587'
#     app.config['MAIL_USE_TLS'] = 'True'
#
#     app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
#     app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # app_config(app)

    db.init_app(app)
    bcrypt.init_app(app)
    loginmanager.init_app(app)
    mail.init_app(app)

    from questionaire.users.routes import users
    from questionaire.questions.routes import qs
    from questionaire.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(qs)
    app.register_blueprint(main)

    return app
