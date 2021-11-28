import telebot
import json
import configparser
import datetime
import schedule
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
    bot.send_message(message.chat.id, 
    "/help для более подробной информации\nПройти тест - /test\nДругие тесты - https://psytests.org/personal/dtla.html")

@bot.message_handler(commands=['help'])
def help(message):
    print(f'[LOG] {str(t.now())} | @{message.from_user.username} help file requested')
    bot.send_message(message.chat.id, "/start - запуск бота\n/test - запустить тестирование\n/report - отправить сообщение об ошибке")

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
        #bot.send_message(message.chat.id, "Тест пройден", reply_markup=keyboard)
        msg = ""
        for i in range(int(data['res'])):
            res = 0
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
            else:
                msg += f"{cur['title']} - акцентуация\n"
        bot.send_message(message.chat.id, f"Тест пройден:\n{msg}", reply_markup=keyboard)
        with open(f'{message.from_user.id}test.json', 'w') as f:
            json.dump(user, f, indent=4)

bot.polling()
