from member import app, db
from flask import render_template, flash
from member.setting.model import UserRegister
from member.setting.form import FormRegister
from member.sendemail import send_mail


@app.route('/', methods=['GET', 'POST'])
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