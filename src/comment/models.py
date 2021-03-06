import datetime

from libs.db import db


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, nullable=False)  # 评论的作者ID
    wid = db.Column(db.Integer, nullable=False)  # 被评论的微博的ID
    cid = db.Column(db.Integer, nullable=False, default=0)  # 回复的评论的ID
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.now())
