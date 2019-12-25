import os
from flask import session
from flask import redirect
from functools import wraps


def save_avatar(nickname, avatar_file):
    base_dir = os.path.dirname(os.path.abspath(__name__))
    file_path = os.path.join(base_dir, 'static', 'upload', nickname)
    avatar_file.save(file_path)


def login_required(views_func):
    @wraps(views_func)
    def check(*args, **kwargs):
        if 'uid' in session:
            return views_func(*args, **kwargs)
        else:
            return redirect('login.html')
    return check
