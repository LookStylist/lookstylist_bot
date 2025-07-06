import os
import telebot
import openai
from flask import Flask, request

# Получение токенов
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка токенов
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set.")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set.")

# Инициализация
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# Вебхук
@app.route("/", methods=["GET"])
def root():
    return "LookStylist bot is up!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "ok", 200
    else:
        return "unsupported content-type", 403

# Команды
@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "👋 Привет! Я LookStylist. Напиши, что хочешь надеть — я подскажу стиль 👗🧥.")

@bot.message_handler(func=lambda msg: True)
def handle_all(message):
    prompt = f"Я покупатель. Хочу совет по одежде. Вот мой запрос: {message.text}. Подскажи как стилист."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"Ошибка: {str(e)}"

    bot.send_message(message.chat.id, reply)

# Локальный запуск (если нужно)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
