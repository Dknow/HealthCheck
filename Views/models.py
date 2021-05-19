# -*- coding: utf-8 -*-


from datetime import datetime

from Views import db

class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {
        'extend_existing': True,
    }
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True,nullable=False)
    password = db.Column(db.String(128), nullable=False)
    update_time = db.Column(db.TIMESTAMP, nullable=False)
    create_time = db.Column(db.DateTime,default = datetime.now,nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = {
        'extend_existing': True,
    }
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(128))
    host = db.Column(db.String(128), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(128))
    password = db.Column(db.String(128))
    device_type= db.Column(db.String(128), nullable=False)
    def _format(self):
        d = {}
        d['id'] = self.id
        d['device_name'] = self.device_name
        d['host'] = self.host
        d['port'] = self.port
        d['user'] = self.user
        d['password'] = self.password
        d['device_type'] = self.device_type

        return d


class result(db.Model):
    __tablename__ = 'result'
    __table_args__ = {
        'extend_existing': True,
    }
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    start_time =db.Column(db.DateTime,default = datetime.now,nullable=False)
    cpu = db.Column(db.Integer)
    """
    other result write hear
    
    """
if __name__ == "__main__":
    db.create_all()