from file_manager import read_json_file, write_json_file
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

    updated_alerts = []
    for a in alerts_json:
        print(a)
        alert = Alert.from_dict(a)
        if not alert.is_notified():
            print(f"Processing alert: {alert.symbol} {alert.condition} {alert.target_price} {alert.convert}")
            send_alert(alert)
            if alert.is_notified():
                print(f"Alert {alert.id} has been notified.")
                continue
        updated_alerts.append(alert)
    
    write_json_file(updated_alerts)
    print("All alerts processed.")
    print("Alerts file updated.")
    print("Scheduled job completed.")