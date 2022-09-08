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

bot = telebot.AsyncTeleBot(TOKEN)
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
    if (call.data == 'Channel'):
        bot.send_message(call.message.chat.id, "Канал тут")
    if (call.data == 'Books'):
        bot.send_message(call.message.chat.id, "Книги тут")
    if (call.data == 'Tests'):
        ChangeAge(call.message)
    if (call.data == 'Diary'):
        bot.send_message(call.message.chat.id, "Дневник тут")
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
        types.InlineKeyboardButton(text="Канал", callback_data='Channel'),
        types.InlineKeyboardButton(text="Литература", callback_data='Books'),
        types.InlineKeyboardButton(text="Тесты", callback_data='Tests')
    )
    keyb.row(
            types.InlineKeyboardButton(text="Дневник тревоги", callback_data='Diary'),
            types.InlineKeyboardButton(text="Специалисты", callback_data='Specialist')
    )
    bot.send_message(message.chat.id, 
    f"Привет, {message.from_user.first_name}\nВас приветствует команда PsyShine! Этот текст надо скопипастить, а мне лень списывать с картинки", reply_markup=keyb)
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
        
@bot.message_handler(commands=['test'])
def test(message, i = 1):
    if (i == 1):
        with open(f'{message.from_user.id}test.json', 'w') as f:
            f.write('{}')
    with open(f'{message.from_user.id}test.json', 'r') as f:
        user = json.load(f)
    if i == 1:
        user['username'] = message.from_user.username
        user['first_name'] = message.from_user.first_name
        user['last_name'] = message.from_user.last_name
        bot.send_message(message.chat.id, 'Акцентуация характера — это чрезмерная выраженность отдельных черт характера и их сочетаний, представляющая крайний вариант психической нормы. У некоторых людей некоторые черты характера столь заострены (акцентуированы), что при определенных обстоятельствах это приводит к однотипным конфликтам и нервным срывам. При акцентуации характера личность становится уязвима не к любым (как при психопатиях), а лишь к определенным травмирующим воздействиям, адресованным так называемому «месту наименьшего сопротивления» данного типа характера при сохранении устойчивости к другим.\n\nОтвечайте, долго не раздумывая, вы можете выбрать один их двух предложенных ответов.')
    if (message.text == "/stop"):
        keyboard = types.ReplyKeyboardRemove();
        bot.send_message(message.chat.id, "Вы остановили прохождение теста. Результаты не будут сохранены!", reply_markup = keyboard)
        return
    if i != 1 and ( message.text != 'Да' and message.text != 'Нет' ):
        with open(f'{message.from_user.id}crash.log', 'a') as f:
            f.write(f'question{str(i - 1)}: Неверный ответ: (Сообщение: \'{message.text}\')\n')
        bot.send_message(message.chat.id, 'Пожалуйста, выберете ответ из предложенных')
        bot.register_next_step_handler(message, test, i)
        return
    if i > 1:
        if message.text == 'Да':
            user[str(i - 1)] = '1'
        else:
            user[str(i - 1)] = '-1'
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    with open('testmain.json', 'r') as f:
        data = json.load(f)
    if (i <= int(data["number"])):
        question = data[str(i)]
        button = types.KeyboardButton(text = "Да")
        keyboard.add(button)
        button = types.KeyboardButton(text = "Нет")
        keyboard.add(button)
        bot.send_message(message.chat.id, question, reply_markup=keyboard)
        i += 1
        with open(f'{message.from_user.id}test.json', 'w') as f:
            json.dump(user, f, indent=4)
        bot.register_next_step_handler(message, test, i)
    else:
        if message.text == 'Да':
            user[str(i - 1)] = '1'
        else: user[str(i - 1)] = '-1'
        keyboard = types.ReplyKeyboardRemove()
        msg = ""
        comm = ""
        print (data['res'])
        for i in range(int(data['res'])):
            res = 0
            print (res)
            for add in data[f'res{i}']['add']:
                if add != 0:
                    res += int(user[str(add)])
            for sub in data[f'res{i}']['sub']:
                if sub != 0:
                    res -= int(user[str(sub)])
            res *= int(data[f'res{i}']['k'])
            cur = data[f'res{i}']
            if res < 13:
                msg += f"{cur['title']} - не выражено\n"
            elif res < 18:
                msg += f"{cur['title']} - средняя степень выраженности\n"
                comm += cur['comm'] + '\n'
            else:
                msg += f"{cur['title']} - акцентуация\n"
                comm += cur['comm'] + '\n'
        print (msg)
        bot.send_message(message.chat.id, f"Тест пройден:\n{msg}", reply_markup=keyboard)
        for lines in comm.split('\n'):
            bot.send_message(message.chat.id, f"{lines}", reply_markup=keyboard)
        with open(f'{message.from_user.id}test.json', 'w') as f:
            json.dump(user, f, indent=4)

try:
    bot.polling()
except Exception as e:
    print(f'[ERR] {str(t.now())} | POLLING FATAL ERROR')
    print(f'[ERR] {str(t.now())} | {str(e)}')

