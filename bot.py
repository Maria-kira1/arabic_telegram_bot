import telebot
import os

TOKEN = os.environ.get("TELEGRAM_TOKEN")

if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не задан!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот запущен!")

print("Бот готов к работе, запускаем polling...")
bot.infinity_polling()
