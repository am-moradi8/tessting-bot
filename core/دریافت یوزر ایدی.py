import telebot
import os

# توکن بات خودتون رو اینجا قرار بدید
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# تابع برای دریافت User ID
@bot.message_handler(commands=['userid'])
def get_user_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"User ID شما: {user_id}")

# شروع بات
bot.polling()