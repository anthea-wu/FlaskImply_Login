from member import app, db, login_manager
from flask import render_template, flash, redirect, url_for, request, redirect, session
from member.setting.model import UserRegister
from member.setting.form import FormRegister, FormLogin, FormChangePWD
from member.sendemail import send_mail
from flask_login import login_user, login_required, current_user, logout_user


# 首頁
@app.route('/')
def index():
    return render_template('index.html')


# 註冊
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


# 使用者認證
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


# 登入
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if current_user.is_authenticated:
        flash('你已經登入過帳號了')
        return redirect(url_for('index'))
    else:
        if form.validate_on_submit():
            user = UserRegister.query.filter_by(email=form.email.data).first()
            if user:
                if user.check_password(form.password.data):
                    session.permanent = True
                    login_user(user, form.remember_me.data)
                    next = request.args.get('next')
                    return redirect(next) if next else redirect(url_for('index'))
                else:
                    flash('錯誤的E-mail或密碼')
            else:
                flash('錯誤的E-mail或密碼')
    return render_template('login/login.html', form=form)


# 登出
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('帳號已登出')
    return redirect(url_for('login'))


# 會員資料
@app.route('/userinfo')
@login_required
def userinfo():
    return render_template('member/userinfo.html')


# 確認帳號啟用狀態
@app.before_request
def before_request():
    if current_user.is_authenticated and not current_user.confirm and request.endpoint not in ['re_userconfirm', 'logout', 'user_confirm', 'index'] and request.endpoint!='static' :
        flash('你的帳號還沒有啟用')
        return render_template('register/unactivate.html')


# 重新寄送認證email
@app.route('/re_userconfirm')
@login_required
def re_userconfirm():
    token = current_user.create_confirm_token()
    send_mail(
        sender='陌上花開',
        recipients=[current_user.email],
        subject='啟用帳號',
        template='mail/welcome',
        mailtype='html',
        user=current_user,
        token=token
    )
    flash('請確認你的註冊信箱，點擊網址來啟用帳號')
    return redirect(url_for('index'))


# 更新密碼
@app.route('/changepwd', methods=['GET', 'POST'])
@login_required
def changepwd():
    form = FormChangePWD()
    if form.validate_on_submit():
        if current_user.check_password(form.password_old.data):
            current_user.password = form.password_new.data
            db.session.add(current_user)
            db.session.commit()
            flash('密碼變更成功！請重新登入')
            return redirect(url_for('logout'))
        else:
            flash('錯誤的舊密碼')
    return render_template('member/changePWD.html', form = form)