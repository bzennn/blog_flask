import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'tmp/app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

CSRF_ENABLED = True
SECRET_KEY = 'e0a6723dea1f41b384c35684b0c84686'

ROLE_USER = {'user': 0, 'moderator': 1, 'admin': 2}

MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

UPLOADS_DEFAULT_DEST = os.path.join(basedir, 'uploads/')

MAX_FILE_SIZE = 2 * 1024 * 1024

POSTS_PER_PAGE = 5

ADMINS = ['dima370794@gmail.com', 'dima370794@yahoo.com']


