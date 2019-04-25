from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from questionaire import db
from questionaire.models import Question, Subject
from questionaire.questions.forms import QuestionForm, QuestionaireForm
from questionaire.questions.utils import show_questionlist, parse_question_options

qs = Blueprint('questions', __name__)


@qs.route("/subject/<subj>")
@login_required
def subj_questions(subj):
    pg = request.args.get('page', 1, type=int)

    question_page = Question.query.filter_by(subj_id=subj).order_by(Question.id.desc()). \
        paginate(per_page=5, page=pg)
    return show_questionlist(question_page, pg, subj)


@qs.route("/questions")
@login_required
def list_questions():
    pg = request.args.get('page', 1, type=int)
    question_page = Question.query.order_by(Question.id.asc()).paginate(per_page=5, page=pg)
    return show_questionlist(question_page, pg)


@qs.route("/questions/<int:question_id>")
def show_question(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question.html', question=question, title="Question " + str(question.id))


@qs.route("/questions/new", methods=['GET', 'POST'])
@login_required
def new_question():
    form = QuestionForm()
    subj_list = [(s.id, s.name) for s in Subject.query.order_by(Subject.name.desc()).all()]
    print('Subjects available for Question')
    for s in subj_list:
        print(s)
    form.subject_list[0:] = subj_list
    form.subj_id.choices = subj_list
    if form.validate_on_submit():
        flash('Your question has been added', 'success')
        question_info = parse_question_options(form.optionlist.data, form.boxh.data, form.boxw.data)
        question = Question(q=form.q.data,
                            points=form.points.data,
                            memo=form.memo.data,
                            type=form.type.data,
                            answer=question_info,
                            subj_id=form.subj_id.data)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.home'))
    elif request.method == 'POST':
        flash('Check Values', 'danger')
    return render_template('create_question.html', title="Add Question", form=form, legend="New Question")


@qs.route("/questions/<int:question_id>/update", methods=['GET', 'POST'])
@login_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    # if question.author != current_user:
    #     abort(403)
    form = QuestionForm()
    subj_list = [(s.id, s.name) for s in Subject.query.order_by(Subject.name.desc()).all()]
    print('Subjects available for Question')
    for s in subj_list:
        print(s)
    form.subject_list[0:] = subj_list
    if form.validate_on_submit():
        question.answer = parse_question_options(form.optionlist.data, form.boxh.data, form.boxw.data)
        question.memo = form.memo.data
        question.q = form.q.data
        question.points = form.points.data
        question.type = form.type.data
        question.subj_id = form.subj_id.data

        db.session.commit()
        flash('Question updated', 'success')
        return redirect(url_for('questions.list_questions'))
    elif request.method == 'GET':
        form.q.data = question.q
        form.points.data = question.points
        form.type.data = question.type
        form.memo.data = question.memo
        form.subj_id.data = question.subj_id
        form.subj_id.choices = subj_list
        form.answer.data = question.answer

    return render_template('create_question.html', title="Update Question", form=form, legend="Update Question")


@qs.route("/questions/<int:question_id>/delete", methods=['POST'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted', 'success')
    return redirect(url_for('questions.list_questions'))


@qs.route("/questionaire", methods=['GET', 'POST'])
@login_required
def new_questionaire():
    form = QuestionaireForm()
    subj_list = [(s.id, s.name) for s in Subject.query.order_by(Subject.name.desc()).all()]
    form.subject_list[0:] = subj_list
    if form.validate_on_submit():
        return redirect(url_for('questions.list_questions'))
    elif request.method == 'POST':
        flash('Check Values', 'danger')
    return render_template('questionaire_form.html', form=form)
