import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')


# Конфигурация базы данных
DB_NAME = 'tasteograph.db'