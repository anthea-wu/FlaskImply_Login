from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, validators, PasswordField, ValidationError
from wtforms.fields.html5 import EmailField
from member.setting.model import UserRegister

class FormRegister(Form):
    username = StringField('帳號', validators=[
        validators.DataRequired(),
        validators.Length(10,30)
    ])
    email = EmailField('E-mail', validators=[
        validators.DataRequired(),
        validators.Length(1,50),
        validators.Email()
    ])
    password = PasswordField('密碼', validators=[
        validators.DataRequired(),
        validators.Length(10,50),
        validators.EqualTo('password2', message='兩次密碼輸入必須相同')
    ])
    password2 = PasswordField('確認密碼', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('註冊帳號')

    def validate_email(self, field):
        if UserRegister.query.filter_by(email=field.data).first():
            raise ValidationError('信箱已被註冊 :-<')
    
    def validate_username(self, field):
        if UserRegister.query.filter_by(username=field.data).first():
            raise ValidationError('帳號已被註冊 :-<')