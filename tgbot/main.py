import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from tgbot.config import BOT_TOKEN
from tgbot.exceptions import WeatherException
from tgbot.schemas import Result
from tgbot.utils import aquery

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

message_template = """
Температура города {city}": <b>{temp}</>
Атмосферное давление: <b>{pressure_mm}</>
Скорость ветра: <b>{wind_speed}</>
"""


class WeatherState(StatesGroup):
    button = State()
    city = State()


@dp.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext) -> None:
    button_text = 'Узнать погоду'
    kb = [
        [types.KeyboardButton(text=button_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await state.set_state(WeatherState.button)
    await message.answer(f"Нажмите на кнопку {button_text}", reply_markup=keyboard)


@dp.message(WeatherState.button)
async def process_city(message: types.Message, state: FSMContext) -> None:
    await state.set_state(WeatherState.city)
    await message.answer("Напишите название города")


@dp.message(WeatherState.city)
async def process_result(message: types.Message, state: FSMContext) -> None:
    url = f'http://127.0.0.1:8000/weather/?city={message.text}'
    try:
        response = await aquery(url=url)
        data = Result.model_validate(response)
        await message.answer(message_template.format(
            city=message.text,
            temp=data.temp,
            pressure_mm=data.pressure_mm,
            wind_speed=data.wind_speed
        ))
    except WeatherException:
        await message.answer('Сервер временно не доступен, попробуйте позже')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
