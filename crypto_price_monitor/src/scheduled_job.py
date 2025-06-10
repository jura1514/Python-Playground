from file_manager import read_json_file
from models import Alert
from notifier import send_alert
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def price_alert_job():
    alerts_json = read_json_file()
    if not alerts_json:
        print("No alerts found.")
        return
    
    alerts = [Alert.from_dict(a) for a in alerts_json]
    print(alerts[0])
    send_alert(alerts[0])
