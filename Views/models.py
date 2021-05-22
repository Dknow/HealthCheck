# -*- coding: utf-8 -*-


from datetime import datetime

from Views import db


# class User(db.Model):
#     __tablename__ = 'user'
#     __table_args__ = {
#         'extend_existing': True,
#     }
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(128), unique=True, nullable=False)
#     password = db.Column(db.String(128), nullable=False)
#     update_time = db.Column(db.TIMESTAMP, nullable=False)
#     create_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
#
#     def __repr__(self):
#         return '<User %r>' % self.username


class Task(db.Model):
    __tablename__ = 'task'
    __table_args__ = {
        'extend_existing': True,
    }
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(128))
    device_id = db.Column(db.Integer)
    cpu = db.Column(db.Boolean)
    mem = db.Column(db.Boolean)
    disk = db.Column(db.Boolean)
    version = db.Column(db.Boolean)
    uptime = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    ssh_connect = db.Column(db.Boolean)

class Result(db.Model):
    __tablename__ = 'result'
    __table_args__ = {
        'extend_existing': True,
    }
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    task_id = db.Column(db.Integer)
    start_time = db.Column(db.DateTime, default=datetime.now, nullable=False)
    cpu = db.Column(db.String(128))
    uptime = db.Column(db.String(128))
    mem = db.Column(db.String(128))
    disk = db.Column(db.String(128))
    ssh_connect = db.Column(db.Boolean)
    version = db.Column(db.String(128))

    """
    other result write hear
    
    """

    def _format(self):
        d = {}
        d['id'] = self.id
        d['device_id'] = self.device_id
        d['task_id'] = self.task_id
        d['start_time'] = self.start_time
        d['cpu'] = self.cpu
        d['uptime'] = self.uptime
        d['mem'] = self.mem
        d['disk'] = self.disk
        d['ssh_connect'] = self.ssh_connect
        return d

class Device(db.Model):
    __tablename__ = 'device'
    __table_args__ = {
        'extend_existing': True,
    }
    id = db.Column(db.Integer, primary_key=True)
    device_name = db.Column(db.String(128))
    host = db.Column(db.String(128), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    user = db.Column(db.String(128))
    password = db.Column(db.String(128))
    device_type = db.Column(db.String(128), nullable=False)
    update_time = db.Column(db.DateTime, default=datetime.now, nullable=False)

    # status = db.Column(db.Boolean)

class EmailHistory(db.Model):
    __tablename__ = 'email_history'
    __table_args__ = {
        'extend_existing': True,
    }
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer)
    warning = db.Column(db.Boolean)
    warning_result = db.Column(db.String(128))
    recive_email = db.Column(db.String(128))
    send_time = db.Column(db.DateTime, default=datetime.now, nullable=False)



if __name__ == "__main__":
    db.create_all()
