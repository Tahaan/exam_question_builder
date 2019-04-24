from datetime import datetime

from flask import current_app

from questionaire import db, loginmanager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as TimedToken


@loginmanager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return 'User("{username}", "{email}", "{img}")'.format(
            username=self.username, email=self.email, img=self.image_file)

    def get_reset_token(self, expires_seconds=1800):
        # s = TimedToken(app.secret_key, expires_seconds)
        s = TimedToken(current_app.config['SECRET_KEY'], expires_seconds)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = TimedToken(current_app.secret_key)
        try:
            token_verify = s.loads(token)
            user_id = token_verify.pop('user_id')
        except Exception as e:
            print(e)
            print(e.__traceback__)
            print(e.__cause__)
            print(e.args)
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'Post("{title}", "{date}")'.format(title=self.title, date=self.date_posted)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    q = db.Column(db.Text(150), nullable=False)
    points = db.Column(db.Integer(), nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False)
    answer = db.Column(db.Text(), nullable=False)
    memo = db.Column(db.Text(), nullable=False)
    subj_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)

    def __repr__(self):
        return 'Question("{q}", "{points}", "{type}")'.format(q=self.q, points=self.points, type=self.type)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return 'Subject("{id}", "{name}")'.format(id=self.id, name=self.name)
