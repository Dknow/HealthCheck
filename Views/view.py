# -*- coding: utf-8 -*-

from flask import request, render_template, session, redirect, url_for
from flask_wtf.csrf import CSRFError
from sqlalchemy import and_
import json

from Views import app, db
from Views.common import logincheck
from Views.models import Task, Result, Device, EmailHistory


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
    deviceItems = []
    devices = Device.query.filter_by().all()
    for i in devices:
        d = {}
        d['id'] = i.id
        d['device_name'] = i.device_name
        d['host'] = i.host
        d['port'] = i.port
        d['user'] = i.user
        d['device_type'] = i.device_type
        d['update_time'] = i.update_time
        deviceItems.append(d)
    return render_template('add_task.html', title="添加任务",deviceItems=deviceItems)


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
    print(data['device_id'])
    new = Task(
        task_name=data.get('task_name'),
        device_id=int(data.get('device_id')),
        cpu=True if data.get('cpu') in (1,"1") else False,
        mem=True if data.get('mem') in (1,"1") else False,
        disk=True if data.get('disk') in (1,"1") else False,
        uptime=True if data.get('uptime') in (1,"1") else False,
        version=True if data.get('version') in (1,"1") else False,
        ssh_connect=True if data.get('ssh_connect') in (1, "1") else False,

    )
    db.session.add(new)
    db.session.flush()
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


@app.route('/task_list', methods=['GET'])
def task_list():
    tasks = Task.query.filter().all()
    items = []
    for i in tasks:
        d = {}
        d['id'] = i.id
        d['task_name'] = i.task_name
        d['device_name'] = ''
        if  i.device_id:
            device  = Device.query.filter_by(id=int(i.device_id)).first()
            if  device:
                d['device_name'] = device.device_name
                d['device_host'] = device.host

        params = []
        if  i.cpu:
            params.append('cpu')
        if  i.disk:
            params.append('disk')
        if  i.mem:
            params.append('mem')
        if i.uptime:
            params.append('uptime')
        if i.version:
            params.append('version')
        if i.ssh_connect:
            params.append('ssh_connect')
        d["params"] = params
        items.append(d)
    return render_template('task_list.html', items=items, title="任务列表")


@app.route('/task_result/<int:task_id>', methods=['GET', "DELETE"])
@app.route('/task_result', methods=['GET', "DELETE"])
def result(task_id=None):
    items = []
    if task_id:
        r = Result.query.filter_by(task_id=task_id).first()
        if r:
            res = {}
            res['id'] = r.id
            res['device_id'] = r.device_id
            res['task_id'] = r.task_id
            res['start_time'] = r.start_time
            res['uptime'] = r.uptime
            res['mem'] = r.mem
            res['ps'] = r.ps
            items.append(res)
    else:
        item_list = Result.query.filter_by().all()
        deviceQuery = Device.query
        for i in item_list:
            res = {}
            res['id'] = i.id
            res['device_id'] = i.device_id
            res['task_id'] = i.task_id
            res['start_time'] = i.start_time
            res['uptime'] = i.uptime
            res['mem'] = i.mem
            res['disk'] = i.disk
            res['cpu'] = i.cpu
            res['version'] = i.version
            res['ssh_connect'] = i.ssh_connect
            if i.device_id:
                device = deviceQuery.filter_by(id=i.device_id).first()
                res['device_name'] = device.device_name
                res['host'] = device.host
            else:
                res['device_name'] = ""
                res['host'] = ""
            items.append(res)

    return render_template('task_result.html', items=items, title="运行结果")


@app.route('/device', methods=['GET'])
def get_device():
    item_list = Device.query.filter_by().all()
    items = []
    for i in item_list:
        d = {}
        d['id'] = i.id
        d['device_name'] = i.device_name
        d['host'] = i.host
        d['port'] = i.port
        d['user'] = i.user
        d['device_type'] = i.device_type
        d['update_time'] = i.update_time

        items.append(d)

    return render_template('device_management.html', title="设备管理", items=items)


@app.route('/add_device', methods=['POST'])
def add_device():
    host = request.form.get('host')
    port = request.form.get('port')
    device_name = request.form.get('device_name')
    user = request.form.get('user')
    password = request.form.get('password')
    device_type = request.form.get('device_type')

    d = Device.query.filter_by(host=host, port=int(port)).first()
    if not d:
        new = Device(
            device_name=device_name,
            host=host,
            port=int(port),
            user=user,
            password=password,
            device_type=device_type
        )
        db.session.add(new)
        db.session.flush()
    # else:
    #     d.device_name = device_name
    #     d.host = host,
    #     d.port = int(port),
    #     d.user = user,
    #     d.password = password,
    #     d.device_type = device_type
    #     db.session.flush()

    return redirect('/device')


@app.route('/message_record', methods=['GET'])
def message_record():
    # 查询邮件发送记录
    items = []
    itmes_list = EmailHistory.query.all()
    for i in itmes_list:
        d = {}
        d['id'] = i.id
        d['device_id'] = i.device_id
        d['warning'] = i.warning
        d['warning_result'] = i.warning_result
        d['send_time'] = i.send_time
        d['recive_email'] = i.recive_email

        items.append(d)
    return render_template('message_record.html', title="邮件记录", items=items)
