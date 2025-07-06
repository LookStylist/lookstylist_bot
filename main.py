import os
import telebot
import openai
from flask import Flask, request

# Получаем токены из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверка на случай, если токены не установлены
if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("TELEGRAM_BOT_TOKEN not set in environment variables.")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY not set in environment variables.")

# Инициализация бота и OpenAI
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Webhook-сервер
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'LookStylist bot is running!'

@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'ok', 200

# Обработка входящих сообщений
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я твой LookStylist. Напиши, что хочешь надеть, и я подскажу.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = f"Я покупатель. Хочу совет по одежде. Вот мой запрос: {message.text}. Подскажи как стилист."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"Ошибка при обращении к OpenAI: {str(e)}"
    
    bot.send_message(message.chat.id, reply)

# Запускаем бота, если это локальный запуск (например, при отладке)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
