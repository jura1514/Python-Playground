import requests


def send_telegram_message(bot_token, chat_id, message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.ok is True:
            print(f"Telegram response: {response.text}")
            return response.ok
        else:
            print(f"Telegram response error: {response.text}")
            return False
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")
        return False
