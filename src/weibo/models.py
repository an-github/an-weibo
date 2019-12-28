import datetime

from libs.db import db


class Weibo(db.Model):
    __tablename__ = 'weibo'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
    n_zan = db.Column(db.Integer, default=0)


class Zan(db.Model):
    __tablename__ = 'zan'

    uid = db.Column(db.Integer, primary_key=True)
    wid = db.Column(db.Integer, primary_key=True)
