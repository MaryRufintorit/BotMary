
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import openai

openai.api_key = "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"
TELEGRAM_TOKEN = "8169196910:AAFs4o08KZOCzMI5FvmEkwuxmeYlJa66SSI"

SYSTEM_PROMPT = """
Ты — переводчик. Пользователь будет отправлять текст на одном из 4 языков: русском, французском, арабском (диалект), бамбара.
Ты должен:
1. Определить язык.
2. Перевести на три других языка.
3. Ответить в формате:

[Исходный язык: Язык]

Французский:
...

Арабский:
...

Бамбара:
...

Отвечай только переводами. Никаких пояснений. Примерно адаптируй стиль к разговорному.
"""

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        translated = response["choices"][0]["message"]["content"]
        await update.message.reply_text(translated)
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    app.run_polling()

if __name__ == "__main__":
    main()
