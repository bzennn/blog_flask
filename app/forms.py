from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, email, EqualTo, length
from .models import User


class LoginForm(FlaskForm):
    email = StringField("email", validators=[InputRequired(), email()])
    password = PasswordField("password", validators=[InputRequired(), length(min=1, max=100)])
    remember_me = BooleanField("remember", default=False)

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        user_obj = User.query.filter_by(email=self.email.data).first()
        if user_obj is None:
            self.email.errors.append('User with such email does not exist.')
            return False
        if user_obj is not None and not user_obj.check_password(password=self.password.data):
            self.password.errors.append('Wrong password.')
            return False
        return True


class RegisterForm(FlaskForm):
    nickname = StringField("nickname", validators=[InputRequired()])
    email = StringField("email", validators=[InputRequired(), email()])
    password = PasswordField("password",
                             validators=[InputRequired(), EqualTo('repeat_password',
                                                                 message='Passwords must match'),
                                         length(min=1, max=100)])
    repeat_password = PasswordField("password_repeat", validators=[InputRequired()])

    def __init__(self, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        user_nickname = User.query.filter_by(nickname=self.nickname.data).first()
        user_email = User.query.filter_by(email=self.email.data).first()
        if user_nickname:
            self.email.errors.append('This nickname already in use.')
            return False
        if user_email:
            self.email.errors.append('This email already in use.')
            return False
        return True


class EditProfileForm(FlaskForm):
    pass


class CreatePostForm(FlaskForm):
    pass
