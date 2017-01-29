# -*- coding: utf-8 -*-

import utils
import telebot
import config
import random
from SQLighter import SQLighter
from musicDB import MusicDb
from upload_files import upload
from encrypt import enctypt,decrypt
from flask import Flask,request
import os


bot = telebot.TeleBot(config.token)

def insert_to_db(message):
    db = SQLighter()
    db.insert_inf(message)
    db.close()


@bot.message_handler(func=lambda message: True ,commands=['code'])
def markup_code(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('Зашифровать')
    markup.add('Расшифровать')
    bot.send_message(message.chat.id, 'Действие', reply_markup=markup)
    utils.set_active_user(message.chat.id, 'active_command')
    insert_to_db(message)



@bot.message_handler(func=lambda message: True, commands=['upload'])
def upload_inf(message):
    db = SQLighter()
    db.export_to_excel()
    s = upload()
    bot.send_message(message.chat.id, s)


@bot.message_handler(func=lambda message: True, commands=['download'])
def download_inf(message):
    db = SQLighter()
    db.export_to_excel()
    f = open('inf.xlsx', 'rb')
    bot.send_document(message.chat.id, f, None)


@bot.message_handler(func=lambda message: True, commands=['game'])
def game(message):
    db_worker = MusicDb()
    row = db_worker.select_single(random.randint(1, utils.count_rows()))
    markup = utils.generate_markup(row[2], row[3])
    bot.send_voice(message.chat.id, row[1], reply_markup=markup)
    utils.set_user_game(message.chat.id, row[2])
    db_worker.close()

@bot.message_handler(func=lambda message: True, commands=['help'])
def help(message):
    bot.send_message(message.chat.id ,'''/game - игра "Угадай мелодию"
/code - шифрование (Шифруйте текст методом Гронсфельда)
/upload - загрузить файл статистики в облако (загружает Excel-ку на DropBox)
/download - присласть файл статистики
/help - обзор команд''')

@bot.message_handler(func=lambda message: True, commands=['check'])
def checkin(message):
    keyboard_hider = telebot.types.ReplyKeyboardRemove()
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Поделись местоположением", reply_markup=keyboard)
    bot.send_message(message.chat.id, 's', reply_markup=keyboard_hider)


@bot.message_handler(func=lambda message: True, commands=['numb'])
def check_numb(message):
    keyboard_hider = telebot.types.ReplyKeyboardRemove()
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = telebot.types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Поделись номером", reply_markup=keyboard)


@bot.message_handler(func=lambda message: True, content_types=["text"])
def active_caesar(message):
    answer = utils.get_active_for_user(message.chat.id)
    answer2 = utils.get_answer_for_user(message.chat.id)
    if answer:
        if message.text == 'Зашифровать':
            utils.finish_active_comand(message.chat.id)
            utils.set_active_user(message.chat.id, 'Зашифровать')
            bot.send_message(message.chat.id, 'Введите слово для шифрования',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
        elif message.text == 'Расшифровать':
            utils.finish_active_comand(message.chat.id)
            utils.set_active_user(message.chat.id, 'Расшифровать')
            bot.send_message(message.chat.id, 'Введите слово для шифрования',
                             reply_markup=telebot.types.ReplyKeyboardRemove())
        else:
            comm = utils.get_active_for_user(message.chat.id)
            if not comm:
                bot.send_message(message.chat.id, 'Ошибка!')
            elif comm == 'Зашифровать':
                bot.send_message(message.chat.id, enctypt(message))
            elif comm == 'Расшифровать':
                bot.send_message(message.chat.id, decrypt(message))
            utils.finish_active_comand(message.chat.id)
    elif answer2:
        keyboard_hider = telebot.types.ReplyKeyboardRemove()
        if message.text == answer2:
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
        else:
            bot.send_message(message.chat.id, 'Увы, Вы не угадали. Попробуйте ещё раз!', reply_markup=keyboard_hider)
        utils.finish_user_game(message.chat.id)
    else:
        bot.send_message(message.chat.id, 'Необходимо ввести команду',
                         reply_markup=telebot.types.ReplyKeyboardRemove())


if __name__ == '__main__':
    utils.count_rows()
    random.seed()
    bot.polling(none_stop=True)







