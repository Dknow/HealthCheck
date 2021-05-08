# -*- coding: utf-8 -*-
from flask import Blueprint

api = Blueprint('api1', __name__)



@api.route('/login', methods=['GET', 'POST'])
def login():

    '''
    check userName & pwd
    set cookie
    :return:
    '''
    pass
    return "login"


@api.route('/login_out', methods=['GET'])
def login_out():
    '''
    reset cookie
    :return:
    '''
    return "login_out"

