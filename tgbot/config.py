import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
SERVER_API = 'http://127.0.0.1:8000/weather/'
