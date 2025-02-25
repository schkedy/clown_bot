import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
GOSHA_USER_ID = int(os.getenv('GOSHA_USER_ID'))
TIMUR_USER_ID = int(os.getenv('TIMUR_USER_ID')) 