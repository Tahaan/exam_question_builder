from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SubjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=200)], default="")
    submit = SubmitField('Save')
