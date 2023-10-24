import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
SERVER_DOMAIN = os.getenv('SERVER_DOMAIN', 'backend')
SERVER_API = f'http://{SERVER_DOMAIN}:8000/weather/'
