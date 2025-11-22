import asyncio
import aiohttp
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

API_TOKEN = os.environ.get("API_TOKEN")


bot = Bot(API_TOKEN)
dp = Dispatcher()


# Функция получения курса доллара
async def get_usd_rate():
    url = "https://api.monobank.ua/bank/currency"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json(content_type=None)

            if not isinstance(data, list):
                print("Ошибка ответа от Monobank:", data)
                return None

            for item in data:
                if (
                    item.get("currencyCodeA") == 840 and 
                    item.get("currencyCodeB") == 980
                ):
                    return item.get("rateSell")

            return None


# Команда /start с кнопкой
@dp.message(Command("start"))
async def start(message: Message):
    kb = ReplyKeyboardBuilder()
    kb.button(text="Курс")
    kb.adjust(1)

    await message.answer("Привет! Нажми кнопку ниже:", reply_markup=kb.as_markup(resize_keyboard=True))


# Обработка кнопки "Курс"
@dp.message()
async def handle_buttons(message: Message):
    if message.text == "Курс":
        rate = await get_usd_rate()
        if rate:
            await message.answer(f"💵 Курс доллара: {rate:.2f} грн")
        else:
            await message.answer("⚠️ Не удалось получить курс.")

    else:
        await message.answer("Нажми кнопку «Курс».")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
