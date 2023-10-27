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
<b>{city}</b>
Температура по Цельсию: <b>{temp}</b>
Атмосферное давление: <b>{pressure_mm}</b>
Скорость ветра: <b>{wind_speed}</b>
"""


class WeatherState(StatesGroup):
    button = State()
    city = State()


button_text = 'Узнать погоду'


def get_button():
    kb = [
        [types.KeyboardButton(text=button_text)]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


@dp.message(CommandStart())
async def command_start(message: types.Message, state: FSMContext) -> None:
    keyboard = get_button()

    await state.set_state(WeatherState.button)
    await message.answer(f"Нажмите на кнопку {button_text}", reply_markup=keyboard)


@dp.message(WeatherState.button)
async def process_city(message: types.Message, state: FSMContext) -> None:
    await state.set_state(WeatherState.city)
    await message.answer("Напишите название города")


@dp.message(WeatherState.city)
async def process_result(message: types.Message, state: FSMContext) -> None:
    try:
        response = await aquery(url=f'{SERVER_API}?city={message.text}')
        result = Result.model_validate(response)
        if result.success == ResultSuccess.ok:
            result_message = message_template.format(
                city=message.text,
                temp=result.data.temp,
                pressure_mm=result.data.pressure_mm,
                wind_speed=result.data.wind_speed
            )
        else:
            result_message = result.message
    except WeatherException:
        result_message = 'Сервер временно не доступен, попробуйте позже'

    keyboard = get_button()
    await state.set_state(WeatherState.button)
    await message.answer(result_message)
    await message.answer(f"Нажмите на кнопку {button_text}", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
