from flask import Blueprint
from flask import request
from flask import redirect
from flask import session

from libs.db import db
from user.logics import login_required
from .models import Comment

comment_bp = Blueprint('comment', import_name='comment')


@comment_bp.route('/post', methods=('POST',))
@login_required
def post():
    uid = session['uid']
    wid = int(request.form.get('wid'))
    content = request.form.get('content')
    cmt = Comment(uid=uid, wid=wid, content=content)
    db.session.add(cmt)
    db.session.commit()
    return redirect('/weibo/show?wid=%s' % wid)