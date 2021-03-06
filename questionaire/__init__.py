from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
loginmanager = LoginManager()
loginmanager.login_view = 'users.login'
loginmanager.login_message_category = 'info'

mail = Mail()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    bcrypt.init_app(app)
    loginmanager.init_app(app)
    mail.init_app(app)

    from questionaire.users.routes import users
    from questionaire.questions.routes import qs
    from questionaire.main.routes import main
    from questionaire.subjects.routes import subj
    from questionaire.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(qs)
    app.register_blueprint(main)
    app.register_blueprint(subj)
    app.register_blueprint(errors)

    return app
