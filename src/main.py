#!/usr/bin/env python
from flask import Flask
from flask import render_template
from libs.db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://an:123456@localhost/py1907'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'M\xd2\x16\xa0K\x01\x0f@\x9f(\xab2V\xd7\xe3\x00'
db.init_app(app)


@app.route('/')
def home():
    return render_template('base.html')


if __name__ == '__main__':
    from user import user_bp

    app.register_blueprint(user_bp)

    app.debug = True
    app.run()
