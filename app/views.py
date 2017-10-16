from flask import render_template, redirect, url_for, flash, session, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from .forms import LoginForm, RegisterForm, EditProfileForm
from .models import User, Post
from app import app, db, login_manager
from config import ROLE_USER


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@app.route('/')
def index():
    text = 'Home Page'
    return render_template('index.html',
                           text=text)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.before_request
def before_request():
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    next = request.args.get('next')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user, form.remember_me.data)
        return redirect(next or url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
def logout():
    if g.user.is_authenticated:
        logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    if g.user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.nickname.data, form.email.data, form.password.data,
                        form.firstName.data, form.lastName.data, datetime.utcnow())
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',
                           title='Sign Up',
                           form=form)


@app.route('/user/<nickname>', methods=['GET', 'POST'])
@login_required
def user_profile(nickname):
    global_role = ROLE_USER
    user = User.query.filter_by(nickname=nickname).first()

    form = EditProfileForm()
    if user is None:
        return abort(404)
    else:
        user_role = user.role

    if form.validate_on_submit():
        user.set_password(form.new_password)
        return redirect(url_for(user_profile(user.nickname)))

    title = nickname
    return render_template('user_profile.html',
                           user=user,
                           global_role=global_role,
                           user_role=user_role,
                           title=title,
                           form=form)
