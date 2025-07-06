import telebot
import openai
from flask import Flask, request

import os

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

app = Flask(__name__)

# Обрабатываем команды и сообщения
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я твой ИИ-стилист. Напиши, что ты ищешь?")

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.send_message(message.chat.id, "Понял! Сейчас подумаю... (тут будет ответ ИИ позже)")

# Webhook обработчик
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# Установка webhook
@app.route('/', methods=['GET'])
def index():
    bot.remove_webhook()
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
    bot.set_webhook(url=webhook_url)
    return "Webhook настроен", 200

# Запуск Flask (в случае локального запуска)
if __name__ == '__main__':
    app.run(debug=True)
