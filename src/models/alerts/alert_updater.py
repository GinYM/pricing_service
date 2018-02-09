from src.common.database import Database
from src.models.alerts.alert import Alert
import os
import src.website_config  as config

Database.initialize()
alerts_needing_update = Alert.find_needing_update()


for alert in alerts_needing_update:
    #if alert.user_email == os.environ.get('ADMIN_EMAIL').replace('\"', ""):
    if alert.user_email == config.ADMIN_EMAIL:
        alert.load_item_price()
        alert.send_email_if_price_reached()
