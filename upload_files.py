# -*- coding: utf-8 -*-

import dropbox
from config import dropb_token


client = dropbox.client.DropboxClient(dropb_token)

def upload():
    f = open('inf.xlsx', 'rb')
    client.file_delete('/active_inf.xlsx')
    client.put_file('/active_inf.xlsx', f)
    return 'Файл с информацией активности загружен на сервер'