from models import Alert, TargetPriceCondition
from monitor import get_price
from telegram_api import send_telegram_message
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_alert(alert: Alert):
    price = get_price(alert.symbol, alert.convert)
    if price is not None:
        priceText = f"Current {alert.symbol} price: {price:.2f} in {alert.convert}"
        print(priceText)

        if (
            alert.condition == TargetPriceCondition.LOWER
            and price <= alert.target_price
        ):
            send_telegram_message(
                TELEGRAM_BOT_TOKEN,
                TELEGRAM_CHAT_ID,
                f"ALERT: {alert.symbol} price dropped to {price:.2f} {alert.convert} (≤ {alert.target_price:.2f})",
            )
            alert.is_notified = True
        elif (
            alert.condition == TargetPriceCondition.HIGHER
            and price >= alert.target_price
        ):
            send_telegram_message(
                TELEGRAM_BOT_TOKEN,
                TELEGRAM_CHAT_ID,
                f"ALERT: {alert.symbol} price rose to {price:.2f} {alert.convert} (≥ {alert.target_price:.2f})",
            )
            alert.is_notified = True

    else:
        print("Failed to retrieve the price.")
