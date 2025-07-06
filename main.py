import telebot
import openai

# Токены
TELEGRAM_BOT_TOKEN = "8045705939:AAFvL0Ucrb-YVeMo7joOwMqIB5s0AA-5kHM"
OPENROUTER_API_KEY = "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"

# Настройка OpenRouter
openai.api_key = OPENROUTER_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

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
            model="openai/gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150,
            temperature=0.7,
            headers={
                "HTTP-Referer": "https://yourdomain.com",  # можешь заменить на свой домен
                "X-Title": "LookStylistBot"
            }
        )
        reply = response.choices[0].message["content"]
    except Exception as e:
        reply = f"❌ Ошибка OpenRouter: {str(e)}"
    bot.send_message(message.chat.id, reply)

if __name__ == '__main__':
    print("🟢 Bot is running via polling...")
    bot.infinity_polling()
