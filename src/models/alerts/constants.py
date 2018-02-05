import os

URL = os.environ.get('MAILGUN_URL')
API_KEY = os.environ.get('MAILGUN_API_KEY')
FROM = os.environ.get('MAILGUN_FORM')
ALERT_TIMEOUT = 0
COLLECTION = "alerts"