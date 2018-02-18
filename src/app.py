from flask import Flask, render_template, session
from src.common.database import Database
from src.models.users.user import User

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "123"

UPLOAD_FOLDER = app.root_path+'/static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.before_first_request
def init_db():
    Database.initialize()


@app.route('/home')
def home():
    if session.get('email') and session['email']:
        user = User.find_by_email(session['email'])
        name = user.user_name
    else:
        name = "Yiming"
    return render_template('home.jinja2', name=name)


@app.route('/')
def hello_world():
    return render_template('index.jinja2')



from src.models.users.views import user_blueprint
from src.models.alerts.views import alert_blueprint
from src.models.stores.views import store_blueprint
from src.models.abouts.views import about_blueprint
from src.models.projects.views import projects_blueprint
from src.models.blogs.views import blogs_blueprint
from src.models.profiles.views import profile_blueprint

app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(about_blueprint, url_prefix="/abouts")
app.register_blueprint(projects_blueprint, url_prefix="/projects")
app.register_blueprint(blogs_blueprint, url_prefix="/blogs")
app.register_blueprint(profile_blueprint, url_prefix="/profiles")