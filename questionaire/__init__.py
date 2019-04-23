import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)
loginmanager.login_view = 'users.login'
loginmanager.login_message_category = 'info'

mail = Mail(app)

from questionaire.users.routes import users
from questionaire.questions.routes import qs
from questionaire.main.routes import main

app.register_blueprint(users)
app.register_blueprint(qs)
app.register_blueprint(main)
