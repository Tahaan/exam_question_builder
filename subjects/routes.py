from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required

from questionaire import db
from questionaire.models import Subject

from subjects.forms import SubjectForm

subj = Blueprint('subjects', __name__)


@subj.route("/subjects/all")
@login_required
def list_subjects():
    pg = request.args.get('page', 1, type=int)
    subject_page = Subject.query.order_by(Subject.subject.desc()).paginate(per_page=5, page=pg)
    return show_subject_list(subject_page, pg)


@subj.route("/subjects/<int:subj_id>")
def show_subject(subj_id):
    subject = Subject.query.get_or_404(subj_id)
    return render_template('subject.html', subject=subject, title="Subject " + str(subject.id))


@subj.route("/subjects/new", methods=['GET', 'POST'])
@login_required
def new_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        flash('New subject added', 'success')
        subject = Subject(name=form.name.data)
        db.session.add(subject)
        db.session.commit()
        return redirect(url_for('main.home'))
    elif request.method == 'POST':
        flash('Check Values', 'danger')
    return render_template('create_subject.html', title="Add Subject", form=form, legend="New Subject")


@subj.route("/subjects/<int:subj_id>/update", methods=['GET', 'POST'])
@login_required
def update_subject(subj_id):
    subject = Subject.query.get_or_404(subj_id)
    form = SubjectForm()
    if form.validate_on_submit():
        subject.name = form.name.data

        db.session.commit()
        flash('Subject updated', 'success')
        return redirect(url_for('subjects.list_subjects'))
    elif request.method == 'GET':
        form.name.data = subject.name

    return render_template('create_subject.html', title="Update Subject", form=form, legend="Update Subject")


@subj.route("/subjects/<int:subj_id>/delete", methods=['POST'])
@login_required
def delete_subject(subj_id):
    s = Subject.query.get_or_404(subj_id)
    db.session.delete(s)
    db.session.commit()
    flash('Subject deleted', 'success')
    return redirect(url_for('subjects.list_subjects'))
