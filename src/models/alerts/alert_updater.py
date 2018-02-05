from src.common.database import Database
from src.models.alerts.alert import Alert

Database.initialize()
alerts_needing_update = Alert.find_needing_update()


for alert in alerts_needing_update:
    print alert.user_email
    if alert.user_email == "jinyiming1996@gmail.com":
        print("Sended!")
        alert.load_item_price()
        alert.send_email_if_price_reached()
