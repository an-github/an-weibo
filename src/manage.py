#!/usr/bin/env python

from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand

from main import app
from libs.db import db
from user.models import User, Follow
from weibo.models import Weibo, Zan
from comment.models import Comment

db.init_app(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def init_db():
    db.create_all()


if __name__ == '__main__':
    manager.run()
