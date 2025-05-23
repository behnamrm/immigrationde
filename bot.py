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

# ✅ Sub items for each checklist item (with icons)
CHECKLIST_SUBITEMS = {
    "1. ℹ️ کسب اطلاعات کلی": [
        "🇩🇪 چرا کشور آلمان؟", "🎓 انواع مقاطع تحصیلی در آلمان", "🗣️ تحصیل به آلمانی یا انگلیسی؟",
        "📄 پذیرش مشروط یا مستقیم؟", "📝 انواع آزمون های زبان آلمانی", "📬 چطور پذیرش بگیریم؟",
        "🎓 بورسیه تحصیلی", "💰 هزینه های زندگی در آلمان", "👨‍💼 کار دانشجویی در آلمان",
        "📊 تبدیل معدل ایران به آلمانی", "💼 بازار کار و درآمد رشته های مختلف در آلمان",
        "🪖 قوانین مشمولان سربازی", "👨‍👩‍👧‍👦 ویزای پیوست به همسر و خانواده"
    ],
    "2. 📄 مدارک مورد نیاز پذیرش": [
        "🗣️ اخذ مدرک زبان", "📝 ترجمه مدارک", "💡 ساخت انگیزه نامه", "📄 ساخت روزمه",
        "🎨 ساخت پورتفولیو", "📨 توصیه نامه از اساتید", "🧾 گواهی سایقه کار",
        "✅ تایید (لگال/بگلا) مدارک ترجمه شده در سفارت"
    ],
    "3. 📬 مراحل اخذ پذیرش": [
        "🏫 دانشگاه یا هوخشوله؟", "📊 رنکینگ دانشگاه های آلمان", "📅 ددلاین پذیرش",
        "🔍 سایت های جستجوی دانشگاه و رشته", "🌐 پذیرش از طریق سایت یونی اسیست",
        "📘 سایت آنابین", "📥 اخذ پذیرش از دانشگاه", "📦 ارسال مدارک به صورت پستی",
        "📝 ثبت نام نهایی در دانشگاه", "🛡️ بیمه دانشجویی", "🏠 گرفتن خوابگاه دانشجویی"
    ],
    "4. 🛂 آمادگی برای سفارت": [
        "📅 گرفتن نوبت سفارت", "📋 چک لیست مدارک روز مصاحبه", "❓ سوالات متداول روز مصاحبه",
        "🗣️ مصاحبه و تحویل ویزا", "⛔ دلایل معمول ریجکتی"
    ],
    "5. ✈️ ورود به آلمان": [
        "🎫 خرید بلیط هواپیما", "🎒 چه وسایلی با خودم ببرم؟", "🛬 فرودگاه و فرم زول",
        "🏠 پیدا کردن خوابگاه و خانه", "📱 خرید سیم کارت در آلمان", "🏢 ثبت محل سکونت (ملده کردن)",
        "🏦 باز کردن حساب بانکی", "🪪 گرفتن کارت اقامت", "🔁 تمدید اقامت بعد از یکسال"
    ]
}

# ✅ توضیحات هر زیرموضوع چک‌لیست
CHECKLIST_CONTENTS = {
    "🇩🇪 چرا کشور آلمان؟": "آلمان یکی از مقصدهای محبوب برای تحصیل به دلایل کیفیت بالا، شهریه کم یا رایگان، و فرصت‌های کاری پس از فارغ‌التحصیلی است.",
    "🎓 انواع مقاطع تحصیلی در آلمان": "در آلمان می‌توان در مقاطع کارشناسی، کارشناسی ارشد و دکترا تحصیل کرد.",
    "🗣️ تحصیل به آلمانی یا انگلیسی؟": "بسته به رشته و دانشگاه، برنامه‌های تحصیلی هم به زبان آلمانی و هم انگلیسی ارائه می‌شوند."
    # 🔁 می‌توانید ادامه دهید برای دیگر موارد
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

# ✅ Split list into rows of n
def split_into_rows(items, row_size=2):
    return [items[i:i+row_size] for i in range(0, len(items), row_size)]

# ✅ Menu handler
async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text

    # Main responses first (to avoid conflict with subitem headers)
    main_responses = {
        "❓ سوالات پرتکرار": "ℹ️ پرسش‌های رایج دانشجویان ایرانی...",
        "🔗 گروه‌های پرسش و پاسخ": "💬 لینک گروه‌های مفید برای پرسش و پاسخ: ...",
        "💼 خدمات مهاجرتی": "🧳 خدمات ما شامل اپلای، ویزا، ترجمه و ...",
        "📬 تماس با ما": "📨 @your_support",
        "📋 مشاهده همه مراحل": "🗂️ همه مراحل مهاجرت: از تحقیق تا ورود به آلمان..."
    }

    if choice in main_responses:
        if choice == "📋 مشاهده همه مراحل":
            all_subitems = sum(CHECKLIST_SUBITEMS.values(), [])
            all_rows = split_into_rows(all_subitems, 3)
            all_rows.append(["🔙 بازگشت به چک‌لیست"])
            await update.message.reply_text(
                "تمام مراحل را انتخاب کنید:",
                reply_markup=ReplyKeyboardMarkup(all_rows, resize_keyboard=True)
            )
        else:
            await update.message.reply_text(main_responses[choice])
        return

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

    if choice in CHECKLIST_SUBITEMS:
        sub_items = CHECKLIST_SUBITEMS[choice]
        sub_menu = split_into_rows(sub_items, 2) + [["🔙 بازگشت به چک‌لیست"]]
        await update.message.reply_text(
            f"لطفا یکی از زیرمجموعه‌های «{choice}» را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(sub_menu, resize_keyboard=True)
        )
        return

    if choice in CHECKLIST_CONTENTS:
        await update.message.reply_text(CHECKLIST_CONTENTS[choice])
        return

    await update.message.reply_text("لطفاً از گزینه‌های منو استفاده کنید.")

# ✅ App startup
if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))
    app.run_polling()
