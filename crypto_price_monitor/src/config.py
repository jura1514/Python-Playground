import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    USE_FILE_STORAGE = os.getenv("USE_FILE_STORAGE", "true")
    DATABASE_URL = os.getenv("DATABASE_URL")
    API_KEY = os.getenv("API_KEY")
    TARGET_PRICE_LOW = float(os.getenv("TARGET_PRICE_LOW", "0"))
    TARGET_PRICE_HIGH = float(os.getenv("TARGET_PRICE_HIGH", "1e10"))
    
