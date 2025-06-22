from cachetools import TTLCache
import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

from config import Config
from models.enums import Convert, Symbol

# import pprint

API_KEY = Config.API_KEY

cache = TTLCache(maxsize=10, ttl=15)

def validate_input(symbol, convert):
    # Validate types
    if not isinstance(symbol, str) or not isinstance(convert, str):
        print("Symbol and convert must be strings.")
        return None

    # Validate values against enums
    if symbol not in Symbol.__members__:
        print(
            f"Invalid symbol: {symbol}. Must be one of: {list(Symbol.__members__.keys())}"
        )
        return None
    if convert not in Convert.__members__:
        print(
            f"Invalid convert: {convert}. Must be one of: {list(Convert.__members__.keys())}"
        )
        return None


def get_price(symbol="BTC", convert="USD"):
    """
    Fetches the current price of a cryptocurrency in a specified currency.

    :param symbol: The cryptocurrency symbol to fetch the price for (default is 'BTC').
    :param convert: The currency to convert the price into (default is 'USD').

    :return: The current price of the cryptocurrency in the specified currency, or None if an error occurs.
    """
    validate_input(symbol, convert)

    cache_key = (symbol, convert)
    if cache_key in cache:
        print(f"Cache hit for {symbol} in {convert}. Returning cached price.")
        return cache[cache_key]

    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    parameters = {"symbol": symbol, "convert": convert}
    headers = {"Accepts": "application/json", "X-CMC_PRO_API_KEY": API_KEY}

    try:
        response = requests.get(url, params=parameters, headers=headers)
        data = response.json()
        # pprint.pprint(data)
        price = data["data"][symbol][0]["quote"][convert]["price"]
        cache[cache_key] = price
        return price
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(f"An error occurred: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
