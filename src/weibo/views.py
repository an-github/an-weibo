import datetime
from math import ceil

from flask import Blueprint, abort
from flask import render_template
from flask import redirect
from flask import request
from flask import session

from libs.db import db
from user.logics import login_required
from user.models import User
from .models import Weibo

weibo_bp = Blueprint('weibo', import_name='weibo')
weibo_bp.template_folder = './tempaltes'


@weibo_bp.route('/')
@weibo_bp.route('/index')
def index():
    page = int(request.args.get('page', 1))
    n_per_page = 10
    offset = (page - 1) * n_per_page
    wb_list = Weibo.query.order_by(Weibo.created.desc()).limit(n_per_page).offset(offset)
    n_wb = Weibo.query.count()
    n_page = 5 if n_wb >= 50 else ceil(n_wb / n_per_page)
    uid_list = {wb.id for wb in wb_list}
    users = dict(User.query.filter(User.id.in_(uid_list)).values('id', 'nickname'))
    return render_template('index.html', page=page, n_page=n_page, users=users, wb_list=wb_list)


@weibo_bp.route('/post', methods=('GET', 'POST'))
@login_required
def post():
    if request.method == 'POST':
        content = request.form.get('content').strip()
        if not content:
            return render_template('post.html', error='内容不能为空')
        else:
            weibo = Weibo(uid=session['uid'], content=content)
            weibo.created = datetime.datetime.now()
            db.session.add_all(weibo)
            db.session.commit()
            return redirect('/weibo/show?wid=%s' % weibo.id)
    else:
        return render_template('post.html')


@weibo_bp.route('/edit')
@login_required
def edit():
    if request.method == 'POST':
        wid = int(request.form.get('wid'))
        content = request.form.get('content').strip()
        if not content:
            return render_template('post.html', error='内容他不能为空')
        else:
            weibo = Weibo.query.get(wid)
            weibo.content = content
            weibo.created = datetime.datetime.now()
            db.session.add(weibo)
            db.session.commit()
            return redirect('/weibo/show?wid=%s' % weibo.id)
    else:
        wid = int(request.args.get('wid'))
        weibo = Weibo.query.get(wid)
        return render_template('edit.html', weibo=weibo)


@weibo_bp.route('/show')
@login_required
def show():
    wid = request.args.get('wid')
    weibo = Weibo.query.get(wid)
    if weibo is None:
        abort(404)
    else:
        user = User.query.get(weibo.uid)
        return render_template('show.html', user=user, weibo=weibo)


@weibo_bp.route('/delete')
@login_required
def delete():
    wid = int(request.args.get('wid'))
    Weibo.query.filter_by(id=wid).delete()
    db.session.commit()
    return redirect('/')
