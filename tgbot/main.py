import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from config import BOT_TOKEN, SERVER_API
from exceptions import WeatherException
from schemas import Result, ResultSuccess
from utils import aquery

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

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
    print('process_result')
    url = f'{SERVER_API}?city={message.text}'
    print(url)
    try:
        response = await aquery(url=url)
        result = Result.model_validate(response)
        if result.success == ResultSuccess.ok:
            await message.answer(message_template.format(
                city=message.text,
                temp=result.data.temp,
                pressure_mm=result.data.pressure_mm,
                wind_speed=result.data.wind_speed
            ))
        else:
            await message.answer(result.message)
    except WeatherException:
        await message.answer('Сервер временно не доступен, попробуйте позже')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
