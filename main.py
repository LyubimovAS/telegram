import os
import requests
import telebot

# Берём токен из Environment Variables
API_TOKEN = os.environ.get("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, могу показать курс доллара.")

# Команда /usd
@bot.message_handler(commands=['usd'])
def get_usd_rate(message):
    url = "https://api.monobank.ua/bank/currency"
    try:
        resp = requests.get(url)
        data = resp.json()
        usd_rate = None
        for item in data:
            if item.get("currencyCodeA") == 840:  # USD
                usd_rate = f"Курс USD: {item.get('rateBuy')} / {item.get('rateSell')}"
                break
        if usd_rate:
            bot.reply_to(message, usd_rate)
        else:
            bot.reply_to(message, "Не удалось получить курс USD.")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")

# Запуск бота
bot.polling(none_stop=True)
