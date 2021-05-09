# -*- coding: utf-8 -*-
import json
from flask import Blueprint, request
from sqlalchemy import and_

api2 = Blueprint('api2', __name__)
from HC.models import Task
from HC import db

@api2.route('/task/<int:id>', methods=['GET'])
def task_get(id=None):
    filter = []
    if id:
        #如果id=0 则返回全部内容
        filter.append(Task.id == id)
    tasks = Task.query.filter(*filter).all()
    res = [t._format() for t in tasks]
    '''
    deviceID
    deviceName
    HOST=''
    PORT=''
    USER=''
    PASSWORD=''
    :return:
    '''

    pass
    return json.dumps({'res': res})


@api2.route('/task', methods=['POST', 'PUT'])
def task_petch():
    '''
    deviceID
    deviceName
    HOST=''
    PORT=''
    USER=''
    PASSWORD=''
    :return:
    '''

    data = json.loads(request.get_data())
    t = Task.query.filter(and_(Task.host == data['host'], Task.port == data['port']))
    if t:
        if request.method == "POST":

            retdata = {'success':True,
                       'msg':'Already exists'}
        else:
            t.update(data)
            db.session.flush()
            retdata = {'success': True}
    else:
        new = Task(
            device_name=data.get('device_name'),
            host = data['host'],
            port = data['port'],
            user = data['user'],
            password = data['password']
        )
        db.session.add(new)
        db.session.flush()
        retdata  = {'success':True}
    return  json.dumps(retdata)


@api2.route('/task/<int:id>', methods=["DELETE"])
def task_del(id):
    '''
    deviceID
    deviceName
    HOST=''
    PORT=''
    USER=''
    PASSWORD=''
    :return:
    '''
    if id:

    pass
    return "task del"


@api2.route('/result', methods=['GET', "DELETE"])
def result():
    '''
    params
    deviceID
    result
        1
        2
        3
        4
        ...

    :return:
    '''
    return 'result'


@api2.route('/report', methods=['POST', "DELETE"])
def report():
    '''

    get result
    :return:
    '''
    return 'report'
