import telebot
from telebot import types

TOKEN = "توکن_تو_اینجا"
CHANNEL_USERNAME = "sexulogyi"
ADMIN_ID = 303268652

bot = telebot.TeleBot(TOKEN)
videos = {}

@bot.message_handler(commands=["start"])
def send_welcome(message):
    if message.from_user.id == ADMIN_ID:
        bot.send_message(message.chat.id, "سلام عشقم، فیلمتو بفرست تا لینکشو برات بسازم.")
    else:
        bot.send_message(message.chat.id, "سلام! برای دریافت فیلم دکمه‌ای که از کانال دریافت کردی رو بزن.")

@bot.message_handler(content_types=["video"])
def save_video(message):
    if message.from_user.id != ADMIN_ID:
        return
    file_id = message.video.file_id
    msg = bot.send_message(message.chat.id, "فیلم ذخیره شد. حالا یه متن بنویس برای دکمه (مثلاً: دریافت فیلم)")
    bot.register_next_step_handler(msg, ask_button_text, file_id)

def ask_button_text(message, file_id):
    button_text = message.text
    unique_code = str(message.message_id) + str(message.from_user.id)
    videos[unique_code] = {"file_id": file_id, "button_text": button_text}
    link = f"https://t.me/{bot.get_me().username}?start={unique_code}"
    bot.send_message(message.chat.id, f"لینک اختصاصی ساخته شد:
{link}")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("/start "))
def handle_start_with_code(message):
    code = message.text.split("/start ")[1]
    if code in videos:
        user_id = message.from_user.id
        member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        if member.status not in ["member", "creator", "administrator"]:
            btn = types.InlineKeyboardMarkup()
            btn.add(types.InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}"))
            bot.send_message(user_id, "برای دیدن فیلم اول عضو کانال شو:", reply_markup=btn)
        else:
            file_id = videos[code]["file_id"]
            caption = "به دلایل فیلترینگ، این ویدیو بعد از ۳۰ ثانیه پاک می‌شود. لطفاً در پیام‌های ذخیره نگه دارید."
            msg = bot.send_video(user_id, file_id, caption=caption)
            bot.register_next_step_handler(msg, lambda m: None)
    else:
        bot.send_message(message.chat.id, "لینک معتبر نیست یا ویدیو حذف شده.")

bot.infinity_polling()
