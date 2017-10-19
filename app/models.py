# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from config import ROLE_USER, DEFAULT_AVATAR_URL


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.SmallInteger, default=ROLE_USER.get('user'))
    email = db.Column(db.String(120), index=True, unique=True)
    pwd_hash = db.Column(db.String(100))
    nickname = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    about_me = db.Column(db.Text)
    registered_on = db.Column(db.DateTime)
    avatar_url = db.Column(db.String, default=DEFAULT_AVATAR_URL, nullable=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    ban_status = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def set_role(self, role):
        self.role = role

    def set_avatar_url(self, avatar_url):
        self.avatar_url = avatar_url

    def __init__(self, nickname, email, password, first_name, last_name, registered_on):
        self.registered_on = registered_on
        self.first_name = first_name
        self.last_name = last_name
        self.nickname = nickname
        self.email = email
        self.set_password(password)

    def __repr__(self):
        return '<User %r>' % self.nickname


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    sub_title = db.Column(db.String(240))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    title_picture_url = db.Column(db.String, default=None, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __init__(self, title, sub_title, body, timestamp, title_picture_url, user_id):
        self.title = title
        self.sub_title = sub_title
        self.body = body
        self.timestamp = timestamp
        self.title_picture_url = title_picture_url
        self.user_id = user_id

    def time_to_string(self, timestamp):
        fmt = '%Y-%m-%d %H:%M'
        return timestamp.strftime(fmt)

    def __repr__(self):
        return '<Post %r>' % self.title


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, body, timestamp, post_id, user_id):
        self.body = body
        self.timestamp = timestamp
        self.post_id = post_id
        self.user_id = user_id

    def time_to_string(self, timestamp):
        fmt = '%Y-%m-%d %H:%M'
        return timestamp.strftime(fmt)

    def __repr__(self):
        return '<Comment %r>' % self.body

