from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from questionaire.models import User

SUBJECT_LIST = [
    ('1', 'Robotics'),
    ('4', 'Electronics'),
    ('3', 'Mechanics'),
    ('2', 'Programming')]


TYPE_LIST = [
    ('entry', 'Simple Input'),
    ('int', 'Integer Number'),
    ('multi', 'Multiple Choice'),
    ('box', 'Picture Box')]


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)],
                           description="Select a username")
    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])

    submit = SubmitField('Update')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different username')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That address is taken. Please choose a different email address')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)],
                           description="Select a username")
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()],
                             description="New password")
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
                                     description="Enter password again")

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different username')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That address is taken. Please choose a different email address')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class QuestionaireForm(FlaskForm):
    qtitle = StringField('Exam Title: ', validators=[DataRequired(), Length(min=2, max=200)],
                         description="Subject and/or date",
                         default="Test")
    time = StringField('Exam Time: ', validators=[DataRequired(), Length(min=2, max=200)],
                       description="Time available",
                       default="100 minutes")
    nr_of_questions = IntegerField('Number of Questions', validators=[])
    subject = SelectField('Subject', validators=[DataRequired()],
                          choices=SUBJECT_LIST)
    instr = TextAreaField('Instructions', description="Write out the questionaire instructions")
    submit = SubmitField('Submit')


class QuestionForm(FlaskForm):
    q = StringField('Question', validators=[DataRequired(), Length(min=2, max=200)],
                    default="? ? ?")
    subject = SelectField('Subject', validators=[DataRequired()],
                          choices=SUBJECT_LIST)
    type = SelectField('Type', validators=[DataRequired()],
                       choices=TYPE_LIST)
    points = IntegerField('Points', validators=[], default=1)
    memo = StringField('Memo', validators=[DataRequired()], default="?")
    answer = StringField('Answer', validators=[DataRequired(), Length(min=2, max=200)],
                    default="?")
    submit = SubmitField('Save')
