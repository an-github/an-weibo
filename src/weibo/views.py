import datetime
from collections import OrderedDict
from math import ceil

from flask import Blueprint, abort
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from libs.db import db
from user.logics import login_required
from user.models import User
from user.models import Follow
from .models import Weibo
from .models import Zan
from comment.models import Comment

weibo_bp = Blueprint('weibo', import_name='weibo')
weibo_bp.template_folder = './templates'


@weibo_bp.route('/')
@weibo_bp.route('/index')
def index():
    page = int(request.args.get('page', 1))
    n_per_page = 10
    offset = (page - 1) * n_per_page
    wb_list = Weibo.query.order_by(Weibo.created.desc()).limit(n_per_page).offset(offset)
    n_weibo = Weibo.query.count()
    n_page = 5 if n_weibo >= 50 else ceil(n_weibo / n_per_page)
    uid_list = {wb.uid for wb in wb_list}
    users = dict(User.query.filter(User.id.in_(uid_list)).values('id', 'nickname'))
    wid_list = {wb.id for wb in wb_list}
    zan_list = []
    if 'uid' in session:
        uid = session['uid']
        for wid in wid_list:
            zan = Zan.query.filter_by(uid=uid, wid=wid).first()
            if zan is None:
                continue
            zid = zan.wid
            zan_list.append(zid)
        return render_template('index.html', page=page, n_page=n_page, wb_list=wb_list, users=users, zan_list=zan_list)
    else:
        return render_template('index.html', page=page, n_page=n_page, wb_list=wb_list, users=users)


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
            db.session.add(weibo)
            db.session.commit()
            return redirect('/')
    else:
        return render_template('post.html')


@weibo_bp.route('/edit', methods=('GET', 'POST'))
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
        comments = Comment.query.filter_by(wid=weibo.id).order_by(Comment.created.desc())
        all_uid = {c.uid for c in comments}
        cmt_users = dict(User.query.filter(User.id.in_(all_uid)).values('id', 'nickname'))
        comments = OrderedDict([[cmt.id, cmt] for cmt in comments])
        return render_template('show.html', weibo=weibo, user=user, cmt_users=cmt_users, comments=comments)


@weibo_bp.route('/delete')
@login_required
def delete():
    wid = int(request.args.get('wid'))
    Weibo.query.filter_by(id=wid).delete()
    db.session.commit()
    return redirect('/')


@weibo_bp.route('/zan')
@login_required
def zan():
    uid = session['uid']
    wid = int(request.args.get('wid'))
    zan = Zan(uid=uid, wid=wid)
    db.session.add(zan)
    try:
        Weibo.query.filter_by(id=wid).update({'n_zan': Weibo.n_zan + 1})
        db.session.commit()
    except (IntegrityError, FlushError):
        db.session.rollback()
        Zan.query.filter_by(uid=uid, wid=wid).delete()
        Weibo.query.filter_by(id=wid).update({'n_zan': Weibo.n_zan - 1})
        db.session.commit()
    last_url = request.referrer or '/weibo/show?wid=%s,%s' % wid
    return redirect(last_url)


@weibo_bp.route('/f_w')
@login_required
def f_w():
    uid = session['uid']
    follow_list = [fid for (fid,) in Follow.query.filter_by(uid=uid).values('fid')]
    page = int(request.args.get('page', 1))
    n_per_page = 10
    offset = (page - 1) * n_per_page
    wb_list = Weibo.query.filter(Weibo.uid.in_(follow_list)).order_by(Weibo.created.desc()).limit(n_per_page).offset(
        offset)
    n_weibo = Weibo.query.filter(Weibo.uid.in_(follow_list)).count()
    n_page = 5 if n_weibo >= 50 else ceil(n_weibo / n_per_page)
    users = dict(User.query.filter(User.id.in_(follow_list)).values('id', 'nickname'))
    return render_template('f_w.html', page=page, n_page=n_page, users=users, wb_list=wb_list)


@weibo_bp.route('/top50')
@login_required
def top50():
    now = datetime.datetime.now()
    start = now - datetime.timedelta(30)
    wb_list = Weibo.query.filter(Weibo.created > start).order_by(Weibo.n_zan.desc()).limit(50)
    uid_list = {wb.id for wb in wb_list}
    users = dict(User.query.filter(User.id.in_(uid_list)).values('id', 'nickname'))
    return render_template('top50.html', wb_list=wb_list, users=users)
