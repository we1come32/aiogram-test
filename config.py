from os import getenv

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN', '')
assert BOT_TOKEN

# Only for redis settings
CACHE_STORAGE = getenv('CACHE_STORAGE', '')

DATABASE = getenv('DATABASE', 'sqlite:///cache.db')

WEATHER_API_TOKEN = getenv('WEATHER_API_TOKEN', '')  # Для сервиса https://www.weatherapi.com
assert WEATHER_API_TOKEN
