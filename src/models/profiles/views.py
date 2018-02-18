from flask import Blueprint, render_template, request, json, url_for, redirect, session
from src.common.utils import Utils
from src.models.users.user import User
import src.models.users.decorators as users_decorator

profile_blueprint = Blueprint('profiles', __name__)


@profile_blueprint.route('/update_username', methods=['GET','POST'])
def update_username():
    if request.method == 'GET':
        return redirect(url_for('.index'))
    else:
        user = User.find_by_email(session['email'])
        if request.form['user_name']:
            user.user_name = request.form['user_name']
            user.save_to_db()
        return redirect(url_for('.index'))


@profile_blueprint.route('/', methods=['POST', 'GET'])
#@users_decorator.require_login
def index():
    user = User.find_by_email(session['email'])
    if user is None:
        return render_template('profiles/error.jinja2')
    if request.method == 'GET':
        user_name = user.user_name
        if user is None:
            bindings = None
        else:
            bindings = user.binding
        return render_template('profiles/profile.jinja2',bindings=bindings,user_name=user_name)
    else:
        email_addr = request.form['email']
        password = request.form['password']
        user_name = user.user_name
        if Utils.check_hashed_password(password, user.password):
            user.add_binding(binding_email=email_addr)
            return render_template('profiles/profile.jinja2', bindings=user.binding,user_name=user_name)
        else:
            return render_template('profiles/error.jinja2')

