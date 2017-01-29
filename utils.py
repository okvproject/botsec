# -*- coding: utf-8 -*-

from config import database_name
import sqlite3
import random
from telebot import types

def set_active_user(chat_id,active):
    with sqlite3.connect(database_name) as cursor:
        insert_string = 'INSERT INTO user_act_comm(chatid,comm) VALUES("{}", "{}")'.format(chat_id,active)
        cursor.execute(insert_string)

def get_active_for_user(chat_id):
    with sqlite3.connect(database_name) as cursor:
        try:
            active  =cursor.execute('SELECT comm FROM user_act_comm WHERE chatid=?',(chat_id,)).fetchall()[0]
            for i in active:
                active = i
            return active
        except IndexError:
            return None

def finish_active_comand(chat_id):
    with sqlite3.connect(database_name) as cursor:
        cursor.execute('DELETE from user_act_comm WHERE chatid =?',(chat_id,))


def count_rows():
    global rowsnum
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    count=c.execute('SELECT count(*) FROM music_game').fetchall()[0]
    for i in count:
        rowsnum =int(i)
    return rowsnum


def set_user_game(chat_id, estimated_answer):
    with sqlite3.connect(database_name) as cursor:
        insert_string = 'INSERT INTO user_in_game(chatid,answer) VALUES("{}", "{}")'.format(chat_id,estimated_answer)
        cursor.execute(insert_string)


def finish_user_game(chat_id):
    with sqlite3.connect(database_name) as cursor:
        cursor.execute('DELETE from user_in_game WHERE chatid =?',(chat_id,))


def get_answer_for_user(chat_id):
    with sqlite3.connect(database_name) as cursor:
        try:
            answer  =cursor.execute('SELECT answer FROM user_in_game WHERE chatid=?',(chat_id,)).fetchall()[0]
            for i in answer:
                answer = i
            return answer
        except IndexError:
            return None


def generate_markup(right_answer, wrong_answer):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    all_answers = '{},{}'.format(right_answer, wrong_answer)
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    random.shuffle(list_items)
    for item in list_items:
        markup.add(item)
    return markup