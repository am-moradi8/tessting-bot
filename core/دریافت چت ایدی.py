import telebot
import os

# توکن بات خودتون رو اینجا قرار بدید
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# تابع برای پاسخ به دستور /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! 😊 به بات من خوش اومدی. برای دریافت Chat ID، دستور /chatid رو ارسال کن.")

# تابع برای دریافت Chat ID
@bot.message_handler(commands=['chatid'])
def get_chat_id(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"Chat ID این گروه/چت: {chat_id}")

# تابع برای پاسخ به پیام‌های متنی
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "سلام":
        bot.reply_to(message, "سلام عزیزم! 😊")
    elif message.text == "چطوری؟":
        bot.reply_to(message, "من خوبم، ممنون! شما چطورین؟ 🌟")
    else:
        bot.reply_to(message, "متوجه نشدم! لطفاً دوباره تلاش کنید.")

# تابع برای حذف پیام‌های خاص (مثال: حذف پیام‌هایی که شامل کلمه "حذف" هستند)
@bot.message_handler(func=lambda message: "حذف" in message.text)
def delete_message(message):
    bot.delete_message(message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "پیام شما حذف شد! ❌")

# شروع بات
bot.polling()