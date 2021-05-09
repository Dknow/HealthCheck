# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hc.sqlite'
db = SQLAlchemy(app, use_native_unicode='utf8',
                session_options={'autoflush': True, 'autocommit': True, 'expire_on_commit': True})

from Views import Users, Scan

app.register_blueprint(Users.api, url_prefix='/')
app.register_blueprint(Scan.api2, url_prefix='/')


@app.route('/')
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    app.run(debug=True, port=8000)
