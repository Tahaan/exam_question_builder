import os


class Config:
    SECRET_KEY = 'd31b4f37bf2b1a8be9f93107c1d27ad083e92b4ed6416866b5487be73765a2b5'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = 'True'

    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    DEBUG = True
    HTTP_PORT = 5000
