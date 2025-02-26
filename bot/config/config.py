import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN') 