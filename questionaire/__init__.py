from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = 'd31b4f37bf2b1a8be9f93107c1d27ad083e92b4ed6416866b5487be73765a2b5'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginmanager = LoginManager(app)
loginmanager.login_view = 'login'
loginmanager.login_message_category = 'info'

from questionaire import routes
