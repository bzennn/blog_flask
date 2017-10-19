from flask import render_template, redirect, url_for, flash, session, request, g, abort
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime
from .forms import LoginForm, RegisterForm, EditProfileForm, CreatePostForm, CreateCommentForm, AddAvatarForm
from .models import User, Post, Comment
from app import app, db, login_manager, images
from config import ROLE_USER, POSTS_PER_PAGE


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
@app.route('/p<int:page>', methods=['GET', 'POST'])
def index(page = 1):
    posts_obj = Post.query.order_by(Post.timestamp.desc())
    last_page = int(posts_obj.count() / POSTS_PER_PAGE + 1)
    if page > last_page:
        return abort(404)
    posts = posts_obj.paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html',
                           posts=posts,
                           last_page=last_page,
                           page=page)

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


@app.route('/<nickname>', methods=['GET', 'POST'])
@app.route('/<nickname>/p<int:page>', methods=['GET', 'POST'])
@login_required
def user_profile(nickname, page = 1):
    global_role = ROLE_USER
    user = User.query.filter_by(nickname=nickname).first()

    if user is None:
        return abort(404)

    posts_obj = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc())
    posts = posts_obj.paginate(page, POSTS_PER_PAGE, False)
    last_page = int(posts_obj.count() / POSTS_PER_PAGE + 1)

    form = EditProfileForm()
    form_av = AddAvatarForm()

    if page > last_page:
        return abort(404)

    if form.validate_on_submit():
        if 'save_password' in request.form:
            user.set_password(form.new_password.data)
            db.session.add(user)
            db.session.commit()
        elif 'delete_post' in request.form:
            redirect(url_for('index'))
    elif form_av.validate_on_submit():
        filename = images.save(request.files['avatar'])
        url = images.url(filename)

        user.set_avatar_url(url)
        db.session.add(user)
        db.session.commit()

    title = nickname
    return render_template('user_profile.html',
                           user=user,
                           global_role=global_role,
                           title=title,
                           form=form,
                           posts=posts,
                           last_page=last_page,
                           page=page,
                           form_av=form_av)


@app.route("/delete_post", methods=['POST'])
@login_required
def delete_post():
    post_id = request.form['post_id']

    p = Post.query.filter_by(id=post_id).first()
    if g.user.nickname != p.author.nickname:
        return abort(404)
    else:
        db.session.delete(p)
        db.session.commit()
        return redirect(url_for('user_profile', nickname=p.author.nickname))
    return redirect(url_for('user_profile', nickname=p.author.nickname))


@app.route('/make-post', methods=['GET', 'POST'])
@login_required
def make_post():

    form = CreatePostForm()
    if g.user is None:
        return abort(404)

    if form.validate_on_submit():
        filename = images.save(request.files['post_picture'])
        url = images.url(filename)
        post = Post(form.post_title.data, form.post_subtitle.data, form.post_content.data, datetime.utcnow(), url, g.user.id)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('user_profile', nickname=g.user.nickname))

    return render_template('make_post.html',
                           form=form,
                           user=g.user)


@app.route('/post/n<post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    if post is None:
        return abort(404)

    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.timestamp.desc()).all()

    form = CreateCommentForm()
    if form.validate_on_submit():
        comment = Comment(form.comment_content.data, datetime.utcnow(), post_id, g.user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post', post_id=post_id))

    return render_template('full_post.html',
                           post=post,
                           form=form,
                           comments=comments)


@app.route('/delete_comment', methods=['POST'])
@login_required
def delete_comment():
    comment_id = request.form['comment_id']

    c = Comment.query.filter_by(id=comment_id).first()
    if g.user.nickname != c.author.nickname:
        return abort(404)
    else:
        db.session.delete(c)
        db.session.commit()
        return redirect(url_for('post', post_id=c.post_id))
    return redirect(url_for('post', post_id=c.post_id))
