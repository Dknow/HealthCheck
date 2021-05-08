# -*- coding: utf-8 -*-


from HC import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True,nullable=False)
    password = db.Column(db.String(128), nullable=False)
    # root = db.Column(db.Integer, nullable=False)
    update_time = db.Column(db.TIMESTAMP, nullable=False)
    create_time = db.Column(db.DateTime,default = datetime.now,nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username
