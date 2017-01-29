# -*- coding: utf-8 -*-

import sqlite3
import config
import xlsxwriter.workbook
from datetime import datetime

class SQLighter:
    def __init__(self):
        self.connection = sqlite3.connect(config.database_name)
        self.cursor = self.connection.cursor()

    def insert_inf(self,message):
        with self.connection:
            insert_string = 'INSERT INTO active_user(id,chat_id, dateT) VALUES(NULL,"{}", "{}")'.format(str(message.chat.id),str(datetime.now()))
            self.cursor.execute(insert_string)
            self.connection.commit()

    def close(self):
        self.connection.close()

    def export_to_excel(self):
        workbook = xlsxwriter.workbook.Workbook('inf.xlsx', {'strings_to_urls': False})
        worksheet = workbook.add_worksheet()
        with self.connection:
            ms =self.cursor.execute('SELECT * FROM active_user')
            for i,row in enumerate(ms):
                for j,value in enumerate(row):
                    worksheet.write(i+1,j,row[j])
        worksheet.write(0, 0, 'id')
        worksheet.write(0, 1, 'Chat_id')
        worksheet.write(0, 2, 'Время запроса')
        workbook.close()