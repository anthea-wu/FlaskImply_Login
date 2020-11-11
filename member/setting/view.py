from member import app, db
from flask import render_template, flash, redirect, url_for, request
from member.setting.model import UserRegister
from member.setting.form import FormRegister, FormLogin
from member.sendemail import send_mail
from flask_login import login_manager


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegister()
    if form.validate_on_submit():
        user = UserRegister(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        token = user.create_confirm_token()

        send_mail(
            sender='陌上花開',
            recipients=[user.email],
            subject='啟用帳號',
            template='mail/welcome',
            mailtype='html',
            user=user,
            token=token
        )

        return render_template('register/successR.html')
    
    return render_template('register/register.html', form=form)



@app.route('/user_confirm/<token>')
def user_confirm(token):
    user = UserRegister()
    data = user.validate_confirm_token(token)
    if data:
        user = UserRegister.query.filter_by(id=data.get('userID')).first()
        user.confirm = True
        db.session.add(user)
        db.session.commit()
        return render_template('register/successT.html')
    else:
        return render_template('register/failT.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if form.validate_on_submit():
        user = UserRegister.query.filter_by(email=form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                return '歡迎登入'
            else:
                flash('錯誤的E-mail或密碼')
        else:
            flash('錯誤的E-mail或密碼')
    return render_template('login/login.html', form=form)
