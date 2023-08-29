# import requests
# from bs4 import BeautifulSoup
import telebot
import time
import datetime
from telebot import types
from selenium import webdriver
# from rest_framework.authtoken.views import ObtainAuthToken
# from account.serializers import LoginSerializer
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext


TOKEN = '5932927064:AAGMmF3hSSenVgFLXkgUu0JSDUT462B9syM' 
bot = telebot.TeleBot(TOKEN)


storage = {}

def store_info(user_id, key, value):
    storage.setdefault(user_id, {})[key] = value

@bot.message_handler(func=lambda message: True)
def process_message(message):
    if message.text == "Категории":
        keyboard3 = types.InlineKeyboardMarkup(row_width=2)
        button = types.InlineKeyboardButton('Избранное', callback_data='2')
        button1 = types.InlineKeyboardButton('Лучшее', callback_data='3')
        button2 = types.InlineKeyboardButton('Поиск', callback_data='4')
        keyboard3.row(button, button1, button2)
        text = '*Категории:*'
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=keyboard3)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        button = telebot.types.KeyboardButton('start')
        markup.add(button)
        text = '*Добро пожаловать на EchoVerse*'
        bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=markup)
        user_id = message.from_user.id
        time.sleep(0.5)
        bot.send_message(message.chat.id, "Введите 'start' чтобы начать")
        bot.register_next_step_handler(message, start)

def start(message):
    if message.text == "start":
        bot.send_message(message.chat.id, "Введите свою почту")
        bot.register_next_step_handler(message, get_email)

def get_email(message):
    user_id = message.from_user.id
    store_info(user_id, "email", message.text)
    
    bot.send_message(message.chat.id, "Введите свой пароль")
    bot.register_next_step_handler(message, get_password)

def get_password(message):
    user_id = message.from_user.id
    store_info(user_id, "password", message.text)
    
    email = storage.get(user_id, {}).get("email")
    password = storage.get(user_id, {}).get("password")
    result = {"email": email, "password": password}
    print(result)
    # проверка
    keyboard1 = types.InlineKeyboardMarkup(row_width=2)
    button1 = types.InlineKeyboardButton('Продолжить', callback_data='1')
    keyboard1.row(button1)
    time.sleep(1)
    text = '*Данные обработанны*'
    bot.send_message(message.chat.id, text, parse_mode='Markdown', reply_markup=keyboard1)


@bot.callback_query_handler(func=lambda call: True)
def handler_callback(call):
    if call.data == "1":
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        button = telebot.types.KeyboardButton('Категории')
        markup.add(button)
        text = '*Добро пожаловать*'
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown', reply_markup=markup)
        time.sleep(0.5)
        keyboard2 = types.InlineKeyboardMarkup(row_width=2)
        button = types.InlineKeyboardButton('Избранное', callback_data='2')
        button1 = types.InlineKeyboardButton('Лучшее', callback_data='3')
        button2 = types.InlineKeyboardButton('Поиск', callback_data='4')
        keyboard2.row(button, button1, button2)
        text = '*Вы успешно залогинелись!*'
        bot.send_message(call.message.chat.id, text, parse_mode='Markdown', reply_markup=keyboard2)


    if call.data == '2':
        bot.send_message(call.message.chat.id, 'Вот песни которые вам нравятся:')
        time.sleep(1)


    if call.data == '3':
        bot.send_message(call.message.chat.id, 'Вот несколько вариантов, которые могут вам понравиться:')


    if call.data == '4':
        bot.send_message(call.message.chat.id, 'Введите название песни:')
        












#########################################################################################################################

    # if message.text == '/espada':
    #     bot.stop_polling()


bot.polling()