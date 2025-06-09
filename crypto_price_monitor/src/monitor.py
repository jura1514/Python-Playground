import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
# import pprint

API_KEY = os.getenv("API_KEY")

def get_price(symbol="BTC", convert="USD"):
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    parameters = {"symbol": symbol, "convert": convert}
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}

    try:
        response = requests.get(url, params=parameters, headers=headers)
        data = response.json()
        # pprint.pprint(data)
        price = data["data"][symbol][0]["quote"][convert]["price"]
        return price
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
