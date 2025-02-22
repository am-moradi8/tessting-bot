import telebot
import os
from telebot.types import *
from pymongo import MongoClient
import matplotlib.pyplot as us
import datetime

API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

client = MongoClient('mongodb://localhost:27017/')

db = client['users']
collection = db['user']


@bot.message_handler(commands=['start'])
def start_bot(message):
    bot.reply_to(message , 'Welcome to the Personal Accountant Bot!\nبه بات حسابدار شخصی خوش آمدید')
    bot.reply_to(message , """برای استفاده و اموزش بر روی عبارت زیر کلیک کنید
                 کلید راهنما /help
                 """)

@bot.message_handler(commands=['help'])
def help_bot(message):
    bot.reply_to(message , """لطفا دستورالعمل زیر را با دقت بخوانید
                 اگر برای اولین بار است که از این بات استفاده میکنید نیاز است ثبت نام کنید
                 کلید ثبت نام /new_user
                 اگر از ثبت نام خود اطمینان حاصل کردید و میخواهید اطلاعات وارد کنید
                 کلید درج اطلاعات /get_new_data
                 اگر اطلاعات خود را به بات داده اید و میخواهید محاسبه انجام شود
                 کلید انجام محاسبات /get_chart
                 """)
    bot.reply_to(message , 'در صورت کار نکردن کلید های بالا میتوانید از منو استفاده کنید')


@bot.message_handler(commands=['new_user'])
def new_user(message):
    user = collection.find_one({'chat_id': str(message.chat.id)})
    if user is not None:
        bot.reply_to(message , """برای ثبت نام اطلاعات خود را به صورت
                 نام و نام خانوادگی-کد ملی-شماره تلفن همراه
                 بفرستید
                 """)
        bot.register_next_step_handler(message, register)

def register(message):
    info = message.text.split('-----')
    name = info[0]
    id = info[1]
    phone = info[2]
    collection.insert_one({
        'chat_id' : str(message.chat.id),
        'user_name' : message.from_user.username,
        'name': name,
        'id': id,
        'phone': phone,
        'income' : [],
        'cost' : [],
        'date' : [],
    })
    bot.reply_to(message , """ثبت نام شما با موفقیت انجام شد
                 حالا میتوانید از بخش /get_chart استفاده کنید
                 """)


@bot.message_handler(commands=['get_new_data'])
def get_new_data(message):
    user = collection.find_one({"chat_id": str(message.chat.id)})
    if user is not None:
        bot.reply_to(message , """اطلاعات هزینه و درآمد خود را به صورت زیر وارد کنید
                     +مقدار عددی درآمد
                     -مقدار عددی هیزنه

                     توجه داشته باشید که درآمد و هزینه را باید باهم وارد کنید
                     اگر درآمدی ندارید به جای آن 
                     +0 قرار دهید
                     """)
        bot.register_next_step_handler(message, database)
    else:
        bot.reply_to(message, "you are not registered . use command in command line")


def database(message):
        user = collection.find_one({"chat_id": str(message.chat.id)})
        if user is not None:
            data = message.text.split("\n")
            income = int(data[0])
            cost = int(data[1]) 
            date = datetime.datetime.now()
            collection.update_one({"chat_id": str(message.chat.id)}, {"$push":{"cost": cost, "income": income, "date": date}})
            bot.reply_to(message, """you can use again get_new_data or get charts""")
        else:
             bot.reply_to(message, "you are not registered . use command in command line")
             bot.reply_to(message , """اطلاعات فردی شما وارد نشد لطفا از دستور
             /help یا /new_user
             استفاده کنید
             """)

@bot.message_handler(commands=['get_chart'])
def get_chart(message):
    user = collection.find_one({'chat_id': str(message.chat.id)})
    if user is not None:
        income = user['income']
        cost = user['cost']
        date = user['date']
        total_income = sum(income)
        total_cost = sum(cost)
        x = income     
        y = cost
        z = date

        us.plot(z, x)

        us.title('Income Chart')
        us.xlabel('Income Date')
        us.ylabel('Income')

        us.savefig(
        'my_plot_income.png',
        dpi=300,
        transparent=True,
        bbox_inches="tight"
    )
        us.plot(z, y)

        us.title('Expense Chart')
        us.xlabel('Expense Date')
        us.ylabel('Expense')

        us.savefig(
        'my_plot_cost.png',
        dpi=300,
        transparent=True,
        bbox_inches="tight"
    )
        bot.reply_to(message, f"your total income : {total_income} \n your total cost : {total_cost} \n your balance : {total_income + total_cost}")
        chart_cost = open("my_plot_cost.png", "rb")
        chart_income = open("my_plot_income.png", "rb")
        bot.send_photo(message.chat.id, chart_income)
        bot.send_photo(message.chat.id, chart_cost)

    else:
        bot.reply_to(message, "you are not registred . check inline command ...")

@bot.message_handler(func=lambda  message: True)
def other_message(message):
    bot.reply_to(message, "input data is not valid . use command in command line")



















bot.infinity_polling()
