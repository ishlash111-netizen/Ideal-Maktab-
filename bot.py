import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from groq import Groq

# .env fayldan muhit o'zgaruvchilarini yuklash
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from groq import Groq

# .env fayldan muhit o'zgaruvchilarini yuklash
load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("8815507111:AAHOYnI5SzYDJFBhBEgI1JaOxj0ooy3UlYc")
GROQ_API_KEY = os.environ.get("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")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

groq_client = Groq(api_key=GROQ_API_KEY)

# TODO: UZUNITED haqida ma'lumotni shu yerga to'ldiring
# (masalan: nima bilan shug'ullanadi, qanday xizmatlar/mahsulotlar,
# qanday savollarga javob berishi kerak va h.k.)
SYSTEM_PROMPT = """Siz UZUNITED nomli tashkilot/jamoa uchun yaratilgan sun'iy \
intellekt yordamchisisiz.

Hozircha UZUNITED haqida batafsil ma'lumot kiritilmagan — shu promptga \
UZUNITED kim ekani, nima bilan shug'ullanishi va foydalanuvchilarga qanday \
yordam berishi kerakligi haqida ma'lumot qo'shing.

Qoidalar:
- Har doim o'zbek tilida, do'stona va aniq javob bering.
- Agar savolga javob berish uchun ma'lumotingiz yetarli bo'lmasa, buni \
to'g'ridan-to'g'ri ayting, o'ylab topmang.
- Javoblarni imkon qadar qisqa va tushunarli qiling."""

# Har bir chat uchun suhbat tarixi (xotirada saqlanadi, bot qayta ishga
# tushirilganda tozalanadi)
chat_histories: dict[int, list[dict]] = {}
MAX_TURNS = 10  # nechta oxirgi savol-javobni eslab qolish


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_histories[update.effective_chat.id] = []
    await update.message.reply_text(
        "Salom! Men UZUNITED sun'iy intellekt botiman 🤖\n\n"
        "Menga istalgan savolingizni yozing — Groq AI orqali javob beraman.\n\n"
        "Buyruqlar:\n"
        "/reset — suhbat tarixini tozalash"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_histories[update.effective_chat.id] = []
    await update.message.reply_text("Suhbat tarixi tozalandi ✅")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    history = chat_histories.setdefault(chat_id, [])
    history.append({"role": "user", "content": user_text})
    # faqat oxirgi MAX_TURNS ta savol-javob juftligini saqlaymiz
    history[:] = history[-MAX_TURNS * 2 :]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        logger.error("Groq API xatoligi: %s", e)
        reply = (
            "Kechirasiz, hozir javob bera olmadim 😔 "
            "Birozdan so'ng qayta urinib ko'ring."
        )

    history.append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN topilmadi. .env faylini to'ldirganingizni tekshiring."
        )
    if not GROQ_API_KEY:
        raise SystemExit(
            "GROQ_API_KEY topilmadi. .env faylini to'ldirganingizni tekshiring."
        )

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
 ")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

groq_client = Groq(api_key=GROQ_API_KEY)

# TODO: UZUNITED haqida ma'lumotni shu yerga to'ldiring
# (masalan: nima bilan shug'ullanadi, qanday xizmatlar/mahsulotlar,
# qanday savollarga javob berishi kerak va h.k.)
SYSTEM_PROMPT = """Siz UZUNITED nomli tashkilot/jamoa uchun yaratilgan sun'iy \
intellekt yordamchisisiz.

Hozircha UZUNITED haqida batafsil ma'lumot kiritilmagan — shu promptga \
UZUNITED kim ekani, nima bilan shug'ullanishi va foydalanuvchilarga qanday \
yordam berishi kerakligi haqida ma'lumot qo'shing.

Qoidalar:
- Har doim o'zbek tilida, do'stona va aniq javob bering.
- Agar savolga javob berish uchun ma'lumotingiz yetarli bo'lmasa, buni \
to'g'ridan-to'g'ri ayting, o'ylab topmang.
- Javoblarni imkon qadar qisqa va tushunarli qiling."""

# Har bir chat uchun suhbat tarixi (xotirada saqlanadi, bot qayta ishga
# tushirilganda tozalanadi)
chat_histories: dict[int, list[dict]] = {}
MAX_TURNS = 10  # nechta oxirgi savol-javobni eslab qolish


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_histories[update.effective_chat.id] = []
    await update.message.reply_text(
        "Salom! Men UZUNITED sun'iy intellekt botiman 🤖\n\n"
        "Menga istalgan savolingizni yozing — Groq AI orqali javob beraman.\n\n"
        "Buyruqlar:\n"
        "/reset — suhbat tarixini tozalash"
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_histories[update.effective_chat.id] = []
    await update.message.reply_text("Suhbat tarixi tozalandi ✅")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    history = chat_histories.setdefault(chat_id, [])
    history.append({"role": "user", "content": user_text})
    # faqat oxirgi MAX_TURNS ta savol-javob juftligini saqlaymiz
    history[:] = history[-MAX_TURNS * 2 :]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        logger.error("Groq API xatoligi: %s", e)
        reply = (
            "Kechirasiz, hozir javob bera olmadim 😔 "
            "Birozdan so'ng qayta urinib ko'ring."
        )

    history.append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)


def main():
    if not TELEGRAM_BOT_TOKEN:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN topilmadi. .env faylini to'ldirganingizni tekshiring."
        )
    if not GROQ_API_KEY:
        raise SystemExit(
            "GROQ_API_KEY topilmadi. .env faylini to'ldirganingizni tekshiring."
        )

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
 
