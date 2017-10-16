# -*- coding: utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from config import ROLE_USER


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
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    ban_status = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.pwd_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd_hash, password)

    def set_role(self, role):
        self.role = role

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
    name = db.Column(db.String(120))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        return '<Post %r>' % self.name


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Comment %r>' % self.body

