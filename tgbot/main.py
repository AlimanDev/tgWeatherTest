import asyncio
import logging

import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from tgbot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)


main_text = 'Узнать погоду'


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text=main_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Нажмите на кнопку {main_text}", reply_markup=keyboard)


@dp.message(F.text == main_text)
async def get_weather(message: types.Message):
    response = requests.get('http://127.0.0.1:8000/weather/')
    data = response.json()
    text = f"""
    Температура: {data['temp']}\n
    """
    await message.answer(text)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
