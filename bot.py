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

# ✅ Sub items for each checklist item
CHECKLIST_SUBITEMS = {
    "1. ℹ️ کسب اطلاعات کلی": [
        "چرا کشور آلمان؟", "انواع مقاطع تحصیلی در آلمان", "تحصیل به آلمانی یا انگلیسی؟",
        "پذیرش مشروط یا مستقیم؟", "انواع آزمون های زبان آلمانی", "چطور پذیرش بگیریم؟",
        "بورسیه تحصیلی", "هزینه های زندگی در آلمان", "کار دانشجویی در آلمان",
        "تبدیل معدل ایران به آلمانی", "بازار کار و درآمد رشته های مختلف در آلمان",
        "قوانین مشمولان سربازی", "ویزای پیوست به همسر و خانواده"
    ],
    "2. 📄 مدارک مورد نیاز پذیرش": [
        "اخذ مدرک زبان", "ترجمه مدارک", "ساخت انگیزه نامه", "ساخت روزمه",
        "ساخت پورتفولیو", "توصیه نامه از اساتید", "گواهی سایقه کار",
        "تایید (لگال/بگلا) مدارک ترجمه شده در سفارت"
    ],
    "3. 📬 مراحل اخذ پذیرش": [
        "دانشگاه یا هوخشوله؟", "رنکینگ دانشگاه های آلمان", "ددلاین پذیرش",
        "سایت های جستجوی دانشگاه و رشته", "پذیرش از طریق سایت یونی اسیست",
        "سایت آنابین", "اخذ پذیرش از دانشگاه", "ارسال مدارک به صورت پستی",
        "ثبت نام نهایی در دانشگاه", "بیمه دانشجویی", "گرفتن خوابگاه دانشجویی"
    ],
    "4. 🛂 آمادگی برای سفارت": [
        "گرفتن نوبت سفارت", "چک لیست مدارک روز مصاحبه", "سوالات متداول روز مصاحبه",
        "مصاحبه و تحویل ویزا", "دلایل معمول ریجکتی"
    ],
    "5. ✈️ ورود به آلمان": [
        "خرید بلیط هواپیما", "چه وسایلی با خودم ببرم؟", "فرودگاه و فرم زول",
        "پیدا کردن خوابگاه و خانه", "خرید سیم کارت در آلمان", "ثبت محل سکونت (ملده کردن)",
        "باز کردن حساب بانکی", "گرفتن کارت اقامت", "تمدید اقامت بعد از یکسال"
    ]
}

# ✅ /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.full_name

    with open("users_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{user_id} - {user_name}\n")

    await update.message.reply_text(
        "سلام 👋\nبه ربات مهاجرت به آلمان خوش آمدید!",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    )

# ✅ Menu handler
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text

    if choice == "📝 چک‌لیست مهاجرت":
        await update.message.reply_text(
            "لطفا دسته‌بندی مورد نظر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(CHECKLIST_MENU, resize_keyboard=True)
        )
        return

    if choice == "🔙 بازگشت به منوی اصلی":
        await update.message.reply_text(
            "بازگشت به منو",
            reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        )
        return

    if choice == "🔙 بازگشت به چک‌لیست":
        await update.message.reply_text(
            "بازگشت به چک‌لیست مهاجرت:",
            reply_markup=ReplyKeyboardMarkup(CHECKLIST_MENU, resize_keyboard=True)
        )
        return

    # Show subitems if applicable
    if choice in CHECKLIST_SUBITEMS:
        sub_items = CHECKLIST_SUBITEMS[choice]
        sub_menu = [[item] for item in sub_items] + [["🔙 بازگشت به چک‌لیست"]]
        await update.message.reply_text(
            f"لطفا یکی از زیرمجموعه‌های «{choice}» را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(sub_menu, resize_keyboard=True)
        )
        return

    # Sub-item example response (optional customization)
    await update.message.reply_text(f"شما گزینه «{choice}» را انتخاب کردید. اطلاعات این بخش در حال آماده‌سازی است.")

    # Main menu responses
    main_responses = {
        "❓ سوالات پرتکرار": "پرسش‌های رایج دانشجویان ایرانی...",
        "🔗 گروه‌های پرسش و پاسخ": "لینک گروه‌های مفید برای پرسش و پاسخ: ...",
        "💼 خدمات مهاجرتی": "خدمات ما شامل اپلای، ویزا، ترجمه و ...",
        "📬 تماس با ما": "@your_support",
        "📋 مشاهده همه مراحل": "همه مراحل مهاجرت: از تحقیق تا ورود به آلمان..."
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
