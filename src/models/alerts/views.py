from flask import Blueprint, render_template, request, session, redirect, url_for

from src.models.alerts.alert import Alert
from src.models.items.item import Item
import src.models.users.decorators as users_decorators

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@users_decorators.require_login
def create_alert():
    if request.method == 'POST':
        name = request.form['name']
        url = request.form['url']

        price_limit = float(request.form['price_limit'])

        item = Item(name, url)

        item.save_to_mongo()
        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()
        return redirect(url_for("users.user_alerts"))
    else:
        return render_template("alerts/new_alert.jinja2")


@alert_blueprint.route('/deactivate/<string:alert_id>')
@users_decorators.require_login
def deactivate_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.deactivate()
    return redirect(url_for("users.user_alerts"))


@alert_blueprint.route('/activate/<string:alert_id>')
@users_decorators.require_login
def activate_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.activate()
    return redirect(url_for("users.user_alerts"))


@alert_blueprint.route('/<string:alert_id>')
@users_decorators.require_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/alert.jinja2', alert=alert)


@alert_blueprint.route('/check_price/<string:alert_id>')
@users_decorators.require_login
def check_alert_price(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.load_item_price()
    return redirect(url_for(".get_alert_page", alert_id=alert_id))


@alert_blueprint.route('/delete/<string:alert_id>')
@users_decorators.require_login
def delete_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    alert.delete()
    return redirect(url_for("users.user_alerts"))


@alert_blueprint.route('/edit/<string:alert_id>', methods=['POST', 'GET'])
@users_decorators.require_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    if request.method == "POST":
        price_limit = float(request.form['price_limit'])
        alert.price_limit = price_limit
        alert.save_to_mongo()
        return redirect(url_for("users.user_alerts"))
    else:
        return render_template("alerts/edit_alert.jinja2", alert=alert)
