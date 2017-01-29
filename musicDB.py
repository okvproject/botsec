# -*- coding: utf-8 -*-

import sqlite3
from config import  database_name

class MusicDb:

    def __init__(self):
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def select_all(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM music_game').fetchall()

    def select_single(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM music_game WHERE id = ?', (rownum,)).fetchall()[0]

    def count_rows(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM music_game').fetchall()
            return len(result)

    def close(self):
        self.connection.close()