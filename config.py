import os

class Config:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_bot_token_here')
    GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS', 'path/to/credentials.json')
    COUPON_EXPIRATION_DAYS = 365*2
    FILE_STORAGE_PATH = os.getenv('FILE_STORAGE_PATH', 'path/to/storage')