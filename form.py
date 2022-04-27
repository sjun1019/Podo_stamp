from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import IntegerField
from wtforms.validators import DataRequired, EqualTo
from models import User #Models.py 가져옴

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    phone = StringField('phone', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('password_2')]) #비밀번호 확인
    password_2 = PasswordField('password_2', validators=[DataRequired()])

class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
            
        def __call__(self, form, field):
            userid = form['userid'].data
            password = field.data
            
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])
    
class DetailForm(FlaskForm):
    userid = StringField('userid', render_kw={'readonly': True})
    phone = StringField('phone', render_kw={'readonly': True})
    name = StringField('name', render_kw={'readonly': True})
    point = IntegerField('point')

class EditForm(FlaskForm):
    userid = StringField('userid', render_kw={'readonly': True})
    phone = StringField('phone', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    point = IntegerField('point', render_kw={'readonly': True})