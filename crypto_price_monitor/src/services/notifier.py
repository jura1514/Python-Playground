from config import Config
from models.enums import Convert, Symbol
from models.models import Alert, TargetPriceCondition
from services.monitor import get_price
from services.telegram_api import send_telegram_message

TELEGRAM_BOT_TOKEN = Config.TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID = Config.TELEGRAM_CHAT_ID


def send_alert(symbol: Symbol, convert: Convert, target_price, condition) -> bool:
    """
    Sends an alert if the current price of the symbol meets the target price condition.

    :param symbol: The cryptocurrency symbol to monitor.
    :param convert: The currency to convert the price into.
    :param target_price: The target price to compare against.
    :param condition: The condition to check (higher or lower than target price).

    :return: True if the alert was sent, False otherwise.
    """
    price = get_price(symbol.value, convert.value)
    if price is not None:
        priceText = f"Current {symbol.value} price: {price:.2f} in {convert.value}"
        print(priceText)

        if condition == TargetPriceCondition.LOWER and price <= target_price:
            send_telegram_message(
                TELEGRAM_BOT_TOKEN,
                TELEGRAM_CHAT_ID,
                f"ALERT: {symbol.value} price dropped to {price:.2f} {convert.value} (≤ {target_price:.2f})",
            )
            return True
        elif condition == TargetPriceCondition.HIGHER and price >= target_price:
            send_telegram_message(
                TELEGRAM_BOT_TOKEN,
                TELEGRAM_CHAT_ID,
                f"ALERT: {symbol.value} price rose to {price:.2f} {convert.value} (≥ {target_price:.2f})",
            )
            return True

        return False

    else:
        print("Failed to retrieve the price.")
        return False
