# coding=utf-8
import telebot
import json
import configparser
import datetime
import threading
import os
import time
from datetime import datetime as t
from telebot import types

print(f'[LOG] {str(t.now())} | Started')
print(f'[LOG] {str(t.now())} | STATUS:  STARTING')
print(f'[LOG] {str(t.now())} | LOADING: LOADING CONFIG')

config = configparser.ConfigParser()
config.read("config.ini")
print(f'[LOG] {str(t.now())} | LOADING: LOADED CONGIF FILE')

TOKEN = config['BOT']['TOKEN']
#CRASHREPORT = config['BOT']['CRASHREPORT']
ADMIN = int(config['BOT']['ADMIN_ID'])
adminpass = config['BOT']['ADMINPASS']

print(f'[LOG] {str(t.now())} | LOADING: CURRENT TOKEN: {TOKEN}')

bot = telebot.TeleBot(TOKEN)
crashreport = telebot.TeleBot(TOKEN)

print(f'[LOG] {str(t.now())} | LOADING: ADMINPASS: {adminpass}')
print(f'[LOG] {str(t.now())} | STATUS:  UP')

with open('book.txt', 'r') as f:
    lines = f.readlines()

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if (call.data == 'back'):
        with open ('users.json', 'r') as f:
                data = json.load(f)
        data[str(call.message.chat.id)] -= 1
        keyb = types.InlineKeyboardMarkup()
        if (data[str(call.message.chat.id)] == 0):
            keyb.add(types.InlineKeyboardButton(text='>', callback_data='forw'))
        else:
            keyb.row(
                    types.InlineKeyboardButton(text='<', callback_data='back'),
                    types.InlineKeyboardButton(text='>', callback_data='forw')
            )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                text=str(lines[data[str(call.message.chat.id)]]), reply_markup=keyb)
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
    if (call.data == 'forw'):
        with open ('users.json', 'r') as f:
            data = json.load(f)
        data[str(call.message.chat.id)] += 1
        keyb = types.InlineKeyboardMarkup()
        if (data[str(call.message.chat.id)] == len(lines) - 1):
            keyb.add(types.InlineKeyboardButton(text='<', callback_data='back'))
        else:
            keyb.row(
                types.InlineKeyboardButton(text='<', callback_data='back'),
                types.InlineKeyboardButton(text='>', callback_data='forw')
            )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
        text=str(lines[data[str(call.message.chat.id)]]), reply_markup=keyb)
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
    if (call.data == 'Twitter'):
        bot.send_message(call.message.chat.id, "В разработке")
    if (call.data == 'Insta'):
            bot.send_message(call.message.chat.id, "В разработке")
    if (call.data == 'Channel'):
        bot.send_message(call.message.chat.id, "Наш канал: @PsyShine")
    if (call.data == 'Methodics'):
        bot.send_message(call.message.chat.id, "В разработке")
    if (call.data == 'Books'):
        bot.send_message(call.message.chat.id, "Раздел в разработке")
    if (call.data == 'Tests'):
        ChangeAge(call.message)
    if (call.data == 'Diary'):
        bot.send_message(call.message.chat.id, "Раздел в разработке")
    if (call.data == 'Specialist'):
        bot.send_message(call.message.chat.id, "Специалисты")
    bot.answer_callback_query(call.id)
    
@bot.message_handler(commands=['report'])
def report(message):
    bot.send_message(message.chat.id, 'Кратко опишите вашу проблему:')
    bot.register_next_step_handler(message, send_report)

def send_report(message):
    print(f'[REP] {str(t.now())} | @{message.from_user.username} reported: {message.text}')
    bot.send_message(ADMIN, f'@{message.from_user.username} - {message.text}')
    bot.send_message(message.chat.id, 'Сообщение отправлено!')

@bot.message_handler(commands=['start'])
def start(message):
    print(f'[LOG] {str(t.now())} | @{message.from_user.username} started')
    keyb = types.InlineKeyboardMarkup()
    keyb.row(
        types.InlineKeyboardButton(text="Канал", url='https://t.me/PsyShine'),
        types.InlineKeyboardButton(text="Instagram", url='https://instagram.com/_psyshine?igshid=YmMyMTA2M2Y='),
        types.InlineKeyboardButton(text="Twitter", callback_data='Twitter')
    )
    keyb.row(
        types.InlineKeyboardButton(text="Специалисты", callback_data='Specialist')
    )
    keyb.row(
        types.InlineKeyboardButton(text="Методики", callback_data='Methodics'),
        types.InlineKeyboardButton(text="Дневник", callback_data='Diary'),
        types.InlineKeyboardButton(text="Литература", callback_data='Books')
        #types.InlineKeyboardButton(text="Тесты", callback_data='Tests')
    )
    
    message_text = f"""
Привет, {message.from_user.first_name}! 
Вас приветствует команда PsyShine.
Мы занимаемся разработкой телеграм-бота, который поможет вам эффективно справиться с тревогой и страхом.
Вы сможете получить достоверную информацию о вашей проблеме, достоверные методики и самое главное - качественную помощь от наших специалистов.
А сейчас мы рады видеть вас здесь. Приятного времяпровождения!
    """
    bot.send_message(message.chat.id, 
    message_text, reply_markup=keyb)
@bot.message_handler(commands=['change_age'])
def ChangeAge(message):
    bot.send_message(message.chat.id, 'Пожалуйста, отправьте свой возраст: ')
    bot.register_next_step_handler(message, change_age)

def change_age(message):
    try: 
        int(message.text)
    except Exception as e:
        print(f'[LOG] {str(t.now())} | An error occured! {str(e)} FROM_USER: {message.from_user.id} {message.from_user.username}')
        return None
    if int(message.text) < 14 and int(message.text) > 11:
        bot.send_message(message.chat.id, 'Вы можете пройти тест. /test')
    elif int(message.text) >= 14 and int(message.text) <= 20:
        bot.send_message(message.chat.id, 'Вы можете пройти тест по ссылке: https://psytests.org/personal/dtla.html')
    else: 
        bot.send_message(message.chat.id, 'Сейчас нет доступных тестов для этой возрастной категории.')

@bot.message_handler(commands=['help'])
def help(message):
    print(f'[LOG] {str(t.now())} | @{message.from_user.username} help file requested')
    bot.send_message(message.chat.id, "/start - запуск бота\n/test - запустить тестирование\n/report - отправить сообщение об ошибке")

@bot.message_handler(commands=['info'])
def info(message):
    with open('users.json', 'r') as f:
        data = json.load(f)
    data[str(message.chat.id)] = 0
    
    keyb = types.InlineKeyboardMarkup()
    keyb.add(types.InlineKeyboardButton(text='>', callback_data='forw'))
    bot.send_message(message.chat.id, lines[0], reply_markup=keyb)
    with open('users.json', 'w') as f:
        json.dump(data, f, indent=4)

try:
    bot.polling()
except Exception as e:
    print(f'[ERR] {str(t.now())} | POLLING FATAL ERROR')
    print(f'[ERR] {str(t.now())} | {str(e)}')

