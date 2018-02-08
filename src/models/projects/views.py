from flask import Blueprint, render_template, request, json, url_for, redirect


projects_blueprint = Blueprint('projects', __name__)


@projects_blueprint.route('/')
def index():
    return render_template('projects/projects.jinja2')