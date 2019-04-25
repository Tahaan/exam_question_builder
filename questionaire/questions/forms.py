from flask import current_app
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, IntegerField, DecimalField, StringField, SubmitField, FieldList
from wtforms.validators import DataRequired, Length, Optional

from questionaire.models import Subject
from questionaire.questions.utils import TYPE_LIST

# class MCOptionForm(FlaskForm):
#     option = StringField('Option', validators=[DataRequired(), Length(max=200)])


def selector_list(app, table):
    with app.app_context():
        items = table.query.orderby(table.name).all()
        return [(i.id, i.name) for i in items]


class QuestionForm(FlaskForm):
    subject_list = []
    q = TextAreaField('Question', validators=[DataRequired(), Length(max=200)], default="")
    subj_id = SelectField('Subject', validators=[DataRequired()],
                          choices=subject_list, coerce=int)
    points = IntegerField('Points', validators=[], default=1)
    type = SelectField('Type', validators=[DataRequired()],
                       choices=TYPE_LIST)
    boxw = IntegerField('Box Width', validators=[], default=500)
    boxh = IntegerField('Box Height', validators=[], default=500)
    memo = TextAreaField('Memo', validators=[DataRequired()], default="")
    numeric = DecimalField('Value', validators=[Optional()])
    answer = StringField('Answer', validators=[Length(max=200)])
    optionlist = FieldList(StringField('Option', validators=[Optional(), Length(max=200)]), min_entries=3)
    submit = SubmitField('Save')


class QuestionaireForm(FlaskForm):
    qtitle = StringField('Exam Title: ', validators=[DataRequired(), Length(min=2, max=200)],
                         description="Subject and/or date",
                         default="Test")
    time = StringField('Exam Time: ', validators=[DataRequired(), Length(min=2, max=200)],
                       description="Time available",
                       default="100 minutes")
    nr_of_questions = IntegerField('Number of Questions', validators=[])
    subject_list = []
    subj_id = SelectField('Subject', validators=[DataRequired()],
                          choices=subject_list, coerce=int),
    instr = TextAreaField('Instructions', description="Write out the questionaire instructions")
    submit = SubmitField('Submit')
