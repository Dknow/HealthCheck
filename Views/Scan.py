# -*- coding: utf-8 -*-
from flask import Blueprint

api = Blueprint('api2', __name__)

@api.route('/task', methods=['GET', 'POST','PUT', "DELETE"])
def task():

    '''
    check userName & pwd
    set cookie
    :return:
    '''
    pass
    return "task"


@api.route('/result', methods=['GET', "DELETE"])
def result():
    '''
    get result
    :return:
    '''
    return 'result'


@api.route('/report', methods=['POST', "DELETE"])
def report():
    '''
    get result
    :return:
    '''
    return 'report'

