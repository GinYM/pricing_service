from flask import Blueprint, render_template, request, json, url_for, redirect, session

from src.models.users.user import User

about_blueprint = Blueprint('abouts', __name__)


@about_blueprint.route('/')
def index():
    if session['email']:
        user = User.find_by_email(session['email'])
        name = user.user_name
    else:
        name = "Yiming"
    return render_template('abouts/about.jinja2', name=name)