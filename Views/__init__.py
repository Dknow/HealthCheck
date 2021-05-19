# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_apscheduler import APScheduler

from Views.config import Config
from Views import task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hc.sqlite'
db = SQLAlchemy(app, use_native_unicode='utf8',
                session_options={'autoflush': True, 'autocommit': True, 'expire_on_commit': True})

app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(64)
csrf = CSRFProtect()
csrf.init_app(app)
app.config.from_object(Config)

scheduler = APScheduler()                  # 实例化 APScheduler
# it is also possible to enable the API directly
# scheduler.api_enabled = True
scheduler.init_app(app)                    # 把任务列表放入 flask
scheduler.start()                          # 启动任务列表

