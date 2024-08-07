from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN', '')
assert BOT_TOKEN

# Only for redis settings
CACHE_STORAGE = getenv('CACHE_STORAGE', '')

DATABASE = getenv('DATABASE', 'sqlite:///cache.db')
