import uuid

from fastapi import FastAPI
from api.main import api_router
from config import Config

from storage.file_manager import write_json_file
from models.models import Alert, TargetPriceCondition
from jobs.scheduled_job import price_alert_job
from storage.sql.db import db_setup

import sys
import time
from models.enums import Symbol, Convert
import schedule
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

USE_FILE_STORAGE = Config.USE_FILE_STORAGE

scheduler = BackgroundScheduler()
trigger = CronTrigger(minute="*")
scheduler.add_job(price_alert_job, trigger)
scheduler.start()

app = FastAPI(
    title="Crypto Price Alert Service",
    description="A service to monitor cryptocurrency prices and send alerts based on user-defined conditions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api", tags=["api"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()


# def write_alerts_to_file():
#     alerts = []
#     alert = Alert(
#         id=uuid.uuid4(),
#         target_price=10000.0,
#         condition=TargetPriceCondition.HIGHER.name,
#         symbol=symbol,
#         convert=convert,
#     )
#     alerts.append(alert)

#     write_json_file([a.__dict__ for a in alerts])


# def write_alerts_to_db():
#     from storage.sql.alert_db import AlertDB
#     from storage.sql.db import SessionLocal

#     session = SessionLocal()
#     try:
#         alert = AlertDB(
#             id=uuid.uuid4(),
#             target_price=10000.0,
#             condition=TargetPriceCondition.HIGHER.name,
#             symbol=symbol,
#             convert=convert,
#             is_notified=False,
#         )
#         session.add(alert)
#         session.commit()
#     except Exception as e:
#         print(f"Error writing alert to database: {e}")
#         session.rollback()
#     finally:
#         session.close()


# def init_jobs():
#     schedule.every().day.at("09:00").do(price_alert_job)
#     schedule.every().day.at("18:00").do(price_alert_job)
#     schedule.every(1).seconds.do(price_alert_job)

#     print(f"Monitoring {symbol} price in {convert}.")
#     print("Scheduled jobs:")
#     print(schedule.get_jobs())


# def get_console_input():
#     try:
#         symbol = Symbol[sys.argv[1].upper()].value if len(sys.argv) > 1 else Symbol.BTC
#         convert = (
#             Convert[sys.argv[2].upper()].value if len(sys.argv) > 2 else Convert.USD
#         )
#         return symbol, convert
#     except KeyError:
#         print("Invalid symbol or currency. Please use a valid option from enums.py.")
#         sys.exit(1)


if __name__ == "__main__":
    pass
    # import uvicorn

    # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

    # (symbol, convert) = get_console_input()

    # if USE_FILE_STORAGE.lower() == "true":
    #     print("Using file storage.")
    #     write_alerts_to_file()
    # else:
    #     print("Using database storage.")
    #     db_setup()
    #     write_alerts_to_db()

    # init_jobs()

    # print("Press Ctrl+C to stop.")

    # try:
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     print("\nStopped monitoring.")
