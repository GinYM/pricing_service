from src.common.database import Database
from src.models.alerts.alert import Alert
import os

Database.initialize()
alerts_needing_update = Alert.find_needing_update()


for alert in alerts_needing_update:
    if alert.user_email == os.environ.get('ADMIN_EMAIL').replace('\"', ""):
        alert.load_item_price()
        alert.send_email_if_price_reached()
