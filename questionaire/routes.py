import os
import uuid

from PIL import Image

from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import redirect
from flask import render_template, url_for, flash, request, abort

from questionaire import app, bcrypt, db
from questionaire.forms import RegistrationForm, LoginForm, QuestionaireForm, UpdateAccountForm, QuestionForm
from questionaire.models import User, Question


@app.route("/")
def home():
    return render_template('home.html', title='Question Machine')


@app.route("/other")
def other():
    return render_template('other.html', title='More About')


@app.route("/maintenance")
def maintenance():
    return render_template('maintenance.html', title='Database Maintenance')


@app.route("/maintenance/clearall")
def wipe_database():
    flash('Database Destroyed - add a new user now', 'danger')
    return redirect(url_for('maintenance'))


@app.route("/maintenance/new")
def create_database():
    db.create_all()
    flash('New Database created', 'info')
    return redirect(url_for('maintenance'))


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return new_user()


@app.route("/users/new", methods=['GET', 'POST'])
def new_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        newuser = User(username=form.username.data,
                       email=form.email.data,
                       password=hashed_pw.decode('UTF-8'))
        db.session.add(newuser)
        db.session.commit()
        flash('Account created for {un}!'.format(un=form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/users/list", methods=['GET', 'POST'])
def user_list():
    return redirect(url_for('other'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        flash('Login failed - Check email and password', 'danger')

    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(uuid.uuid4()) + f_ext
    picture_path = os.path.join(app.root_path, 'static', 'profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename=os.path.join('profile_pics', current_user.image_file))
    return render_template('account.html', image_file=image_file, form=form)


@app.route("/questions")
@login_required
def questions():
    questions = Question.query.all()
    question_list = [{'q': i.q, 'points': i.points, 'a': i.answer, 'type': i.type, 'memo': i.memo, 'id': i.id} for i in questions]

    for n, q in enumerate(question_list):
        q.update({'nr': n+1})
    return render_template('questions.html', questions=question_list)


@app.route("/questions/<int:question_id>")
def question(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question.html', question=question, title="Question " + str(question.id))


@app.route("/questionaire", methods=['GET', 'POST'])
@login_required
def new_questionaire():
    form = QuestionaireForm()
    if form.validate_on_submit():
        return redirect(url_for('questions'))
    elif request.method == 'POST':
        flash('Check Values', 'danger')
    return render_template('questionaire_form.html', form=form)


@app.route("/questions/new", methods=['GET', 'POST'])
@login_required
def new_question():
    form = QuestionForm()
    if form.validate_on_submit():
        flash('Your question has been added', 'success')
        question = Question(q=form.q.data,
                            points=form.points.data,
                            memo=form.memo.data,
                            type=form.type.data,
                            answer=form.answer.data,
                            subject=form.subject.data)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'POST':
        flash('Check Values', 'danger')
    return render_template('create_question.html', title="Add Question", form=form, legend="New Question")


@app.route("/questions/<int:question_id>/update", methods=['GET', 'POST'])
@login_required
def update_question(question_id):
    question = Question.query.get_or_404(question_id)
    # if question.author != current_user:
    #     abort(403)
    form = QuestionForm()
    if form.validate_on_submit():
        question.answer = form.answer.data
        question.memo = form.memo.data
        question.q = form.q.data
        question.points = form.points.data
        question.type = form.type.data
        question.subject = form.subject.data

        db.session.commit()
        flash('Question updated', 'success')
        return redirect(url_for('questions'))
    elif request.method == 'GET':
        form.q.data = question.q
        form.points.data = question.points
        form.type.data = question.type
        form.memo.data = question.memo
        form.subject.data = question.subject
        form.answer.data = question.answer

    return render_template('create_question.html', title="Update Question", form=form, legend="Update Question")


@app.route("/questions/<int:question_id>/delete", methods=['POST'])
@login_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted', 'success')
    return redirect(url_for('questions'))
