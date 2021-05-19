# -*- coding: utf-8 -*-

from flask import request, render_template, session, redirect, url_for
from flask_wtf.csrf import CSRFError
from sqlalchemy import and_
import json

from Views import app,db
from Views.common import logincheck
from Views.models import Task

@app.route('/login', methods=['GET', 'POST'])
@app.route('/', methods=['GET'])
def login():
    '''
    check userName & pwd
    set login status
    :return:
    '''
    if request.method == 'GET':
        return render_template('login.html')
    else:
        account = request.form.get('account')
        password = request.form.get('password')
        if account == app.config.get('ACCOUNT') and password == app.config.get('PASSWORD'):
            session['login'] = 'loginsuccess'
            return redirect(url_for('task_list'))
        else:
            return redirect(url_for('login'))


@app.route('/loginout')
@logincheck
def LoginOut():
    session['login'] = ''
    return redirect(url_for('login'))


@app.route('/Dashboard')
@logincheck
def Dashboard():
    return render_template('Dashboard.html')


@app.route('/404')
def NotFound():
    return render_template('404.html')


@app.route('/500')
def Error():
    return render_template('500.html')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    print('csrf handle error: {}.'.format(str(e)))
    return redirect(url_for('Error'))


# 任务列表页面
@app.route('/task')
# @logincheck
def task():
    filter = []
    # if id:
    # 如果id=0 则返回全部内容
    # filter.append(Task.id == id)
    tasks = Task.query.filter(*filter).all()
    res = [t._format() for t in tasks]
    retdata = {
        'item': {'count': 1, }}
    return render_template('task2.html', **retdata)


@app.route('/add_task', methods=['GET'])
def task_add():
    return render_template('add_task.html')


@app.route('/task_list', methods=['GET'])
def task_list():
    tasks = Task.query.filter().all()
    retdata = {'items': [t._format for t in tasks]}
    return render_template('task_list.html', **retdata)


@app.route('/add_task', methods=['POST', 'PUT'])
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
    data = request.form
    t = Task.query.filter(and_(Task.host == data['host'], Task.port == int(data['port']))).all()
    if t:
        if request.method == "POST":

            retdata = {'success': True,
                       'msg': 'Already exists'}
        else:
            t.update(data)
            db.session.flush()
            retdata = {'success': True}
    else:
        new = Task(
            device_name=data.get('device_name'),
            host=data['host'],
            port=data['port'],
            user=data['user'],
            password=data['password']
        )
        db.session.add(new)
        db.session.flush()
        retdata = {'success': True}
    # return json.dumps(retdata)
    return redirect(url_for('task_list'))


@app.route('/task/<int:id>', methods=["DELETE"])
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
        t = Task.query.filter_by(id=id).first()
        db.session.delete(t)
        db.session.flush()
    else:
        pass
    retdata = {'success': True}
    return json.dumps(retdata)


@app.route('/task_result', methods=['GET', "DELETE"])
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
    retdata = {}
    return render_template('task_result.html', **retdata)


@app.route('/report', methods=['POST', "DELETE"])
def report():
    '''

    get result
    :return:
    '''
    return 'report'
