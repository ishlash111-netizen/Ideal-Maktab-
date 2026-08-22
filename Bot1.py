import os
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from groq import Groq

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = "8815507111:AAHOYnI5SzYDJFBhBEgI1JaOxj0ooy3UlYc"
GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.1-8b-instant"

groq_client = Groq(api_key=GROQ_API_KEY)

# Guruh ID raqamini shu yerga yozing (Bot qo'shilgan guruh IDsi)
TARGET_GROUP_ID = -100xxxxxxxxxx # O'zingizning guruh ID raqamingizni yozing

# Admin paroli va holatlar lug'ati
ADMIN_PASSWORD = "OA77"
admin_sessions = set() # Parolni to'g'ri kiritgan adminlar ro'yxati

# --- Start va Parol tekshirish ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in admin_sessions:
        admin_sessions.remove(user_id) # Har safar start bosganda parolni qayta so'rashi uchun
    
    await update.message.reply_text(
        "Salom! Men UZUNITED yordamchi botiman 🤖\n\n"
        "AI bilan gaplashish uchun shunchaki savol yozing.\n"
        "Admin panelga kirish uchun **OA77** parolini yuboring."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    # 1. Agar foydalanuvchi parolni kiritayotgan bo'lsa
    if user_text == ADMIN_PASSWORD:
        admin_sessions.add(user_id)
        await update.message.reply_text(
            "🔓 **Admin panelga xush kelibsiz!**\n\n"
            "Guruhga yubormoqchi bo'lgan xabaringizni yozing, va men uni avtomatik ravishda guruhga tashlab beraman."
        )
        return

    # 2. Agar foydalanuvchi admin bo'lsa va guruhga xabar yubormoqchi bo'lsa
    if user_id in admin_sessions:
        if TARGET_GROUP_ID == -100xxxxxxxxxx:
            await update.message.reply_text("⚠️ Xatolik: Kodda TARGET_GROUP_ID (guruh ID raqami) ko'rsatilmagan!")
            return
        
        try:
            # Xabarni guruhga yuborish
            await context.bot.send_message(chat_id=TARGET_GROUP_ID, text=user_text)
            await update.message.reply_text("✅ Xabar guruhga muvaffaqiyatli yuborildi!")
        except Exception as e:
            await update.message.reply_text(f"❌ Xatolik yuz berdi: {e}")
        return

    # 3. Oddiy foydalanuvchilar uchun Groq AI javobi
    try:
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": user_text}],
            temperature=0.7,
        )
        reply = response.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("AI hozir javob bera olmayapti, birozdan so'ng qayta urinib ko'ring.")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
