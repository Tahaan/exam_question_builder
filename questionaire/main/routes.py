from flask import Blueprint, render_template, redirect, url_for, flash

from questionaire import db

main = Blueprint('main', __name__)


@main.route("/")
def home():
    return render_template('home.html', title='Question Machine')


@main.route("/other")
def other():
    return render_template('other.html', title='More About')


@main.route("/maintenance")
def maintenance():
    return render_template('maintenance.html', title='Database Maintenance')


@main.route("/maintenance/clearall")
def wipe_database():
    db.drop_all()
    flash('Database Destroyed - add a new user now', 'danger')
    return redirect(url_for('maintenance'))


@main.route("/maintenance/new")
def create_database():
    db.create_all()
    flash('New Database created', 'info')
    return redirect(url_for('maintenance'))


@main.route("/about")
def about():
    return render_template('about.html')


@main.route("/users/list", methods=['GET', 'POST'])
def user_list():
    return redirect(url_for('other'))
