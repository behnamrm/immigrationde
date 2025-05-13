import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Menu options
MAIN_MENU = [
    ["📝 چک‌لیست مهاجرت", "❓ سوالات پرتکرار"],
    ["🔗 گروه‌های بیشتر", "📞 درخواست تماس"],
    ["💼 خدمات مهاجرتی", "🌐 وب‌سایت ما"],
    ["📬 تماس با ما"]
]

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name

    # Log user info
    with open("users_log.txt", "a") as f:
        f.write(f"{user_id} - {user_name}\n")

    await update.message.reply_text(
        "سلام 👋\\nبه ربات مهاجرت به آلمان خوش آمدید!",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    )

# Fallback handler
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    responses = {
        "📝 چک‌لیست مهاجرت": "در اینجا چک‌لیست کامل مهاجرت به آلمان را می‌بینید...",
        "❓ سوالات پرتکرار": "پرسش‌های رایج دانشجویان ایرانی...",
        "🔗 گروه‌های بیشتر": "لینک گروه‌های مفید: ...",
        "📞 درخواست تماس": "لطفاً شماره‌ خود را ارسال کنید. تیم ما با شما تماس می‌گیرد.",
        "💼 خدمات مهاجرتی": "خدمات ما شامل اپلای، ویزا، ترجمه و ...",
        "🌐 وب‌سایت ما": "www.example.com",
        "📬 تماس با ما": "@your_support"
    }

    await update.message.reply_text(responses.get(choice, "لطفاً از گزینه‌های منو استفاده کنید."))

# Main function
if __name__ == '__main__':
    from telegram.ext import MessageHandler, filters

    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    app.run_polling()
