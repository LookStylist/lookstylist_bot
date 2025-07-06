import os
import telebot
import openai

# Получение токенов
TELEGRAM_BOT_TOKEN = "8045705939:AAFvL0Ucrb-YVeMo7joOwMqIB5s0AA-5kHM"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set")

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(
        message.chat.id,
        "👗 Привет! Я LookStylist. Напиши, что хочешь надеть — я подскажу стиль 🧠🛍."
    )

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
        reply = f"❌ Ошибка OpenAI: {str(e)}"
    bot.send_message(message.chat.id, reply)

if __name__ == '__main__':
    print("🟢 Bot is running via polling...")
    bot.infinity_polling()
