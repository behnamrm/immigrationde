import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# ✅ Main menu (right-to-left)
MAIN_MENU = [
    ["❓ سوالات پرتکرار", "📝 چک‌لیست مهاجرت"],
    ["🔗 گروه‌های پرسش و پاسخ", "💼 خدمات مهاجرتی"],
    ["📬 تماس با ما"]
]

# ✅ Checklist submenu (with correct numbering and icons)
CHECKLIST_MENU = [
    ["1. ℹ️ کسب اطلاعات کلی", "2. 📄 مدارک مورد نیاز پذیرش"],
    ["3. 📬 مراحل اخذ پذیرش", "4. 🛂 آمادگی برای سفارت"],
    ["5. ✈️ ورود به آلمان", "📋 مشاهده همه مراحل"],
    ["🔙 بازگشت به منوی اصلی"]
]

# ✅ /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name

    # Log user info
    with open("users_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{user_id} - {user_name}\n")

    await update.message.reply_text(
        "سلام 👋\nبه ربات مهاجرت به آلمان خوش آمدید!",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    )

# ✅ Menu handler
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text

    # Show checklist submenu
    if choice == "📝 چک‌لیست مهاجرت":
        await update.message.reply_text(
            "لطفا دسته‌بندی مورد نظر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(CHECKLIST_MENU, resize_keyboard=True)
        )
        return

    # Return to main menu
    if choice == "🔙 بازگشت به منوی اصلی":
        await update.message.reply_text(
            "بازگشت به منو",
            reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        )
        return

    # Checklist submenu responses
    checklist_responses = {
        "1. ℹ️ کسب اطلاعات کلی": "در این بخش اطلاعات کلی درباره مهاجرت به آلمان را می‌خوانید...",
        "2. 📄 مدارک مورد نیاز پذیرش": "لیست مدارک مورد نیاز برای اخذ پذیرش دانشگاهی...",
        "3. 📬 مراحل اخذ پذیرش": "گام‌های لازم برای گرفتن پذیرش را اینجا ببینید...",
        "4. 🛂 آمادگی برای سفارت": "چطور برای وقت سفارت و مصاحبه آماده شوید...",
        "5. ✈️ ورود به آلمان": "راهنمایی‌های اولیه برای زندگی در آلمان پس از ورود...",
        "📋 مشاهده همه مراحل": "همه مراحل مهاجرت: از تحقیق تا ورود به آلمان..."
    }

    if choice in checklist_responses:
        await update.message.reply_text(checklist_responses[choice])
        return

    # Main menu responses
    main_responses = {
        "❓ سوالات پرتکرار": "پرسش‌های رایج دانشجویان ایرانی...",
        "🔗 گروه‌های پرسش و پاسخ": "لینک گروه‌های مفید برای پرسش و پاسخ: ...",
        "💼 خدمات مهاجرتی": "خدمات ما شامل اپلای، ویزا، ترجمه و ...",
        "📬 تماس با ما": "@your_support"
    }

    if choice in main_responses:
        await update.message.reply_text(main_responses[choice])
    else:
        await update.message.reply_text("لطفاً از گزینه‌های منو استفاده کنید.")

# ✅ App startup
if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    app.run_polling()
