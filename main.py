import os
import requests
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Берём токен из Environment Variables
API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# Создаём клавиатуру с кнопкой "Курс"
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
btn_usd = KeyboardButton("Курс USD")
keyboard.add(btn_usd)

# ---------------------------
# Команда /start
# ---------------------------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Выбери действие:", reply_markup=keyboard)

# ---------------------------
# Обработчик текстовых сообщений
# ---------------------------
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Курс USD":
        url = "https://api.monobank.ua/bank/currency"
        try:
            resp = requests.get(url)
            data = resp.json()
            usd_rate = None
            for item in data:
                if isinstance(item, dict) and item.get("currencyCodeA") == 840:
                    usd_rate = f"Курс USD: {item.get('rateBuy')} / {item.get('rateSell')}"
                    break
            if usd_rate:
                bot.reply_to(message, usd_rate)
            else:
                bot.reply_to(message, "Не удалось получить курс USD.")
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")
    else:
        bot.reply_to(message, "Нажми кнопку 'Курс USD', чтобы узнать курс доллара.")

# ---------------------------
# Запуск бота
# ---------------------------
bot.polling(none_stop=True)
