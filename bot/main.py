import json
import requests
import telebot
import time
from decouple import config


bot = telebot.TeleBot(config("TOKEN"))
BASE_URL = config("BASE_URL")


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    button = telebot.types.KeyboardButton('/register')
    button2 = telebot.types.KeyboardButton('/login')
    button3 = telebot.types.KeyboardButton('/activate')
    markup.add(button, button2, button3)
    text = '*Добро пожаловать на EchoVerse*'
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)

@bot.message_handler(commands=['register'])
def register(message: telebot.types.Message):
    resp = bot.send_message(message.chat.id, "Введите email")
    bot.register_next_step_handler(resp, register_step_2, {})

def register_step_2(message: telebot.types.Message, other_data: dict):
    other_data["email"] = message.text
    resp = bot.send_message(message.chat.id, "Введите password")
    bot.register_next_step_handler(resp, register_step_3, other_data)

def register_step_3(message: telebot.types.Message, other_data: dict):
    other_data["password"] = message.text
    other_data["password_confirm"] = message.text
    resp = bot.send_message(message.chat.id, "Введите username")
    bot.register_next_step_handler(resp, finish_register, other_data)

def finish_register(message: telebot.types.Message, other_data: dict):
    other_data["name"] = message.text
    resp = requests.post(BASE_URL + "/account/register/", other_data)
    if resp.status_code == 400:
        text = ""
        for k, v in resp.json().items():
            text += f"[{k}] {' '.join(v)}\n"
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "Пройдите регистрацию заново /register")
    else:
        bot.send_message(message.chat.id, "Вы успешно зарегались, проверьте почту, после введите команду /activate и введите код для активации аккаунта")

@bot.message_handler(commands=['activate'])
def activate(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Введите email и код через пробел")
    bot.register_next_step_handler(message, send_activation_code)

def send_activation_code(message: telebot.types.Message):
    try:
        email, code = message.text.strip().split()
    except ValueError:
        bot.send_message(message.chat.id, "Введите через один пробел email, затем код")
        return activate(message)
    resp = requests.post(BASE_URL + "/account/activate/", {"email": email, "code": code})
    if resp.status_code == 201:
        bot.send_message(message.chat.id, "Вы успешно активировали аккаунт, перейдите на сайт:")
        bot.send_message(message.chat.id, "/")
    else:
        bot.send_message(message.chat.id, "Email или код не верные")


@bot.message_handler(commands=['login'])
def login(message: telebot.types.Message):
    bot.send_message(message.chat.id, "Введите email и password через пробел")
    bot.register_next_step_handler(message, finish_login)

def finish_login(message: telebot.types.Message):
    try:
        email, password = message.text.strip().split()
    except ValueError:
        bot.send_message(message.chat.id, "Введите через один пробел email, затем password")
        return login(message)
    resp = requests.post(BASE_URL + "/account/login/", {"email": email, "password": password})
    if resp.status_code == 200:
        bot.send_message(message.chat.id, "Вы успешно залогинелись, перейдите на сайт:")
        bot.send_message(message.chat.id, "/")
        with open("db.json") as f:
            if text := f.read():
                db = json.loads(text)
            else:
                db = {}
        db[email] = resp.json()["token"]
        with open("db.json", "w") as f:
            json.dump(db, f)
    else:
        bot.send_message(message.chat.id, "не верные данные")

bot.polling()