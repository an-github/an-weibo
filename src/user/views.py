import datetime

from flask import Blueprint
from flask import request
from flask import render_template
from flask import redirect
from flask import session
from sqlalchemy.exc import IntegrityError

from libs.db import db
from libs.utils import gen_password, check_password
from .models import User
from .logics import save_avatar

user_bp = Blueprint('user', import_name='user')
user_bp.template_folder = './templates'


@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()
        gender = request.form.get('gender', '').strip()
        bio = request.form.get('bio', '').strip()
        city = request.form.get('city', '').strip()
        birthday = request.form.get('birthday', '').strip()
        avatar = request.files.get('avatar')
        user = User(
            nickname=nickname,
            password=gen_password(password),
            gender=gender if gender in ['male', 'female'] else 'male',
            bio=bio,
            city=city,
            birthday=birthday,
            avatar='/static/upload/%s' % nickname,
            created=datetime.datetime.now()
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return render_template('register.html', error='昵称错误')
        save_avatar(nickname, avatar)
        return redirect('/user/login')
    else:
        return render_template('register.html')


@user_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        nickname = request.form.get('nickname', '').strip()
        password = request.form.get('password', '').strip()

        user = User.query.filter_by(nickname=nickname).first()
        if user is None:
            return render_template('login.html', error='用户名有误，请重新输入')
        if check_password(password, user.password):
            session['uid'] = user.id
            return redirect('/user/info')
        else:
            return render_template('login.html', error='密码有误，请重新输入')
    else:
        if 'uid' in session:
            return redirect('/user/info')
        else:
            return render_template('login.html')


@user_bp.route('/logout')
def logout():
    session.pop('uid')
    return redirect('/')


@user_bp.route('/info')
def info():
    uid = session.get('uid')
    if uid:
        user = User.query.get(uid)
        return render_template('info.html', user=user)
    else:
        return render_template('login.html', error='清登陆')
