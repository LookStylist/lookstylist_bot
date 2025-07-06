import os
import telebot
import openai
from flask import Flask, request

# Загружаем переменные окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set in environment variables")

# Инициализация
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY
app = Flask(__name__)

# Проверка работоспособности
@app.route('/', methods=['GET'])
def index():
    return 'LookStylist bot is live', 200

# Обработка Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'OK', 200
    return 'Unsupported Media Type', 415

# Обработка команд
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "👗 Привет! Я LookStylist. Напиши, что хочешь надеть — я подскажу стиль 🧠🛍.")

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    prompt = f"👤 Я покупатель. Хочу совет по одежде. Вот мой запрос: {message.text}. Подскажи как стилист."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"Ошибка от OpenAI: {str(e)}"
    bot.send_message(message.chat.id, reply)

# Запуск для локальной отладки
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
