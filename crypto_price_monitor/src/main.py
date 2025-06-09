from dotenv import load_dotenv
load_dotenv()

import sys
import time
from monitor import get_price
from notifier import send_telegram_message
from enums import Symbol, Convert
import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if __name__ == "__main__":
    try:
        symbol = (
            Symbol[sys.argv[1].upper()].value if len(sys.argv) > 1 else Symbol.BTC.value
        )
        convert = (
            Convert[sys.argv[2].upper()].value
            if len(sys.argv) > 2
            else Convert.USD.value
        )
    except KeyError:
        print("Invalid symbol or currency. Please use a valid option from enums.py.")
        sys.exit(1)

    interval = 300  # 5 minutes

    print(
        f"Monitoring {symbol} price in {convert} every {interval // 60} minutes. Press Ctrl+C to stop."
    )
    try:
        while True:
            price = get_price(symbol, convert)
            if price is not None:
                priceText = f"Current {symbol} price: {price:.2f} in {convert}"
                print(priceText)
                TELEGRAM_BOT_TOKEN
                TELEGRAM_CHAT_ID

                send_telegram_message(
                    TELEGRAM_BOT_TOKEN,
                    TELEGRAM_CHAT_ID,
                    priceText,
                )
            else:
                print("Failed to retrieve the price.")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nStopped monitoring.")
