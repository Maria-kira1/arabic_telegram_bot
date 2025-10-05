import telebot
import os
import openai

# ====== Настройки ======
TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # можно оставить пустым, если не используешь OpenAI

if not TOKEN:
    print("Ошибка: TELEGRAM_TOKEN не задан!")
    exit(1)

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

bot = telebot.TeleBot(TOKEN)

# ====== Команды бота ======
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот запущен! Добро пожаловать 😊")

@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Привет! Я работаю на Render 😊")

# Пример команды с OpenAI (если ключ задан)
@bot.message_handler(commands=['ask'])
def ask_openai(message):
    if not OPENAI_API_KEY:
        bot.send_message(message.chat.id, "OpenAI API ключ не задан.")
        return

    # Берем текст после команды
    question = message.text.replace("/ask", "").strip()
    if not question:
        bot.send_message(message.chat.id, "Напиши вопрос после команды /ask")
        return

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=question,
            max_tokens=100
        )
        answer = response.choices[0].text.strip()
        bot.send_message(message.chat.id, answer)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при обращении к OpenAI: {e}")

# ====== Сообщения, которые не команды ======
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Вы сказали: {message.text}")

# ====== Запуск ======
print("Бот готов к работе, запускаем polling...")
bot.infinity_polling()
