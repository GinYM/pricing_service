from flask import Blueprint, render_template, request, json, url_for, redirect


about_blueprint = Blueprint('abouts', __name__)


@about_blueprint.route('/')
def index():
    return render_template('abouts/about.jinja2')