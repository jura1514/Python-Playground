from models import Alert, TargetPriceCondition
from monitor import get_price
from telegram_api import send_telegram_message
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_alert(alert: Alert):
    price = get_price(alert.symbol.value, alert.convert.value)
    if price is not None:
        priceText = f"Current {alert.symbol.value} price: {price:.2f} in {alert.convert.value}"
        print(priceText)

        if (
            alert.condition == TargetPriceCondition.LOWER
            and price <= alert.target_price
        ):
            send_telegram_message(
                TELEGRAM_BOT_TOKEN,
                TELEGRAM_CHAT_ID,
                f"ALERT: {alert.symbol.value} price dropped to {price:.2f} {alert.convert.value} (≤ {alert.target_price:.2f})",
            )
            alert.set_notified()
        elif (
            alert.condition == TargetPriceCondition.HIGHER
            and price >= alert.target_price
        ):
            send_telegram_message(
                TELEGRAM_BOT_TOKEN,
                TELEGRAM_CHAT_ID,
                f"ALERT: {alert.symbol} price rose to {price:.2f} {alert.convert} (≥ {alert.target_price:.2f})",
            )
            alert.set_notified()

    else:
        print("Failed to retrieve the price.")
