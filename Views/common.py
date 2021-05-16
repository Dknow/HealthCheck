# -*- coding: UTF-8 -*-

from functools import wraps
from flask import session, url_for, redirect, logging


# 登录状态检查
def logincheck(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if 'login' in session.keys():
                if session['login'] == 'loginsuccess':
                    return f(*args, **kwargs)
                else:
                    return redirect(url_for('login'))
            else:
                return redirect(url_for('login'))
        except Exception as e:
            print(e)
            return redirect(url_for('Error'))

    return wrapper
