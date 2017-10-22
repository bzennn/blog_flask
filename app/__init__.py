from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, UPLOADS_DEFAULT_DEST, MAX_FILE_SIZE

app = Flask(__name__)
app.config.from_object('config')

#app.config['PREFERRED_URL_SCHEME'] = 'http'
#app.config['SERVER_NAME'] = '185.143.173.132'

app.config['UPLOADS_DEFAULT_DEST'] = UPLOADS_DEFAULT_DEST
images = UploadSet('images', IMAGES)
configure_uploads(app, images)
patch_request_class(app, MAX_FILE_SIZE)


db = SQLAlchemy(app)


migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = [MAIL_USERNAME, MAIL_PASSWORD]
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'blog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/blog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('blog startup')

from app import views, models
