from config import Config
from storage.file_manager import read_json_file, write_json_file
from models.models import Alert
from services.notifier import send_alert

from storage.sql.db import SessionLocal
from storage.sql.queries import get_alerts

TELEGRAM_BOT_TOKEN = Config.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = Config.TELEGRAM_CHAT_ID
USE_FILE_STORAGE = Config.USE_FILE_STORAGE


def price_alert_job():
    if USE_FILE_STORAGE.lower() == "true":
        alerts_json = read_json_file()
        if not alerts_json:
            print("No alerts found.")
            return

        updated_alerts = []
        for a in alerts_json:
            print(a)
            alert = Alert.from_dict(a)
            if not alert.is_notified():
                print(
                    f"Processing alert: {alert.symbol} {alert.condition} {alert.target_price} {alert.convert}"
                )
                is_sent = send_alert(
                    alert.symbol, alert.convert, alert.target_price, alert.condition
                )
                if is_sent:
                    alert.set_notified()
                    print(f"Alert {alert.id} has been notified.")
                    continue
            updated_alerts.append(alert)

        write_json_file(updated_alerts)
    else:
        session = SessionLocal()
        try:
            alerts = get_alerts(session)
            print(f"Found {len(alerts)} alerts to process.")
            if not alerts:
                print("No alerts found.")
                return

            for alert in alerts:
                print(
                    f"Processing alert: {alert.symbol} {alert.condition} {alert.target_price} {alert.convert}"
                )
                is_sent = send_alert(
                    alert.symbol, alert.convert, alert.target_price, alert.condition
                )
                if is_sent:
                    alert.is_notified = True
                    print(f"Alert {alert.id} has been notified.")
                    continue

            session.commit()
        except Exception as e:
            print(f"Error processing alerts: {e}")
            session.rollback()
        finally:
            session.close()

    print("All alerts processed.")
    print("Scheduled job completed.")
