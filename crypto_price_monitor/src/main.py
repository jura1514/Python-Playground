import os
import uuid
from dotenv import load_dotenv

from storage.file_manager import write_json_file
from models import Alert, TargetPriceCondition
from scheduled_job import price_alert_job
from storage.sql.db import db_setup

load_dotenv()

import sys
import time
from enums import Symbol, Convert
import schedule

USE_FILE_STORAGE = os.getenv("USE_FILE_STORAGE")

def write_alerts_to_file():
    alerts = []
    alert = Alert(
        id=uuid.uuid4(),
        target_price=10000.0,
        condition=TargetPriceCondition.HIGHER.name,
        symbol=symbol,
        convert=convert,
    )
    alerts.append(alert)

    write_json_file([a.__dict__ for a in alerts])


def write_alerts_to_db():
    from storage.sql.alert_db import AlertDB
    from storage.sql.db import SessionLocal

    session = SessionLocal()
    try:
        alert = AlertDB(
            id=uuid.uuid4(),
            target_price=10000.0,
            condition=TargetPriceCondition.HIGHER.name,
            symbol=symbol,
            convert=convert,
            is_notified=False,
        )
        session.add(alert)
        session.commit()
    except Exception as e:
        print(f"Error writing alert to database: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    try:
        symbol = (
            Symbol[sys.argv[1].upper()].value if len(sys.argv) > 1 else Symbol.BTC
        )
        convert = (
            Convert[sys.argv[2].upper()].value
            if len(sys.argv) > 2
            else Convert.USD
        )
    except KeyError:
        print("Invalid symbol or currency. Please use a valid option from enums.py.")
        sys.exit(1)

    if USE_FILE_STORAGE.lower() == "true":
        print("Using file storage.")
        write_alerts_to_file()
    else:
        print("Using database storage.")
        db_setup()
        write_alerts_to_db()

    schedule.every().day.at("09:00").do(price_alert_job)
    schedule.every().day.at("18:00").do(price_alert_job)
    schedule.every(1).seconds.do(price_alert_job)

    print(f"Monitoring {symbol} price in {convert}.")
    print("Scheduled jobs:")
    print(schedule.get_jobs())
    print("Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped monitoring.")
