from functools import wraps

from flask import url_for, session, redirect, request
import src.config as config


def require_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user',next=request.path))
        return func(*args,**kwargs)
    return decorated_function


def require_admin_permission(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in config.ADMINS:
            return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)
    return decorated_function







