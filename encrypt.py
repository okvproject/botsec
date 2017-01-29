# -*- coding: utf-8 -*-

def get_key(text):
    key = 684
    str_key = str(key)
    t = text
    a=len(str_key)
    b =  len(text)
    if a<b:
        while a < b:
            c = b - a
            str_key += str_key[:c]
            a = len(str_key)
    elif a>b:
        str_key = str_key[:b]
    return int(str_key)

def enctypt(message):
    a = message.text
    shift = str(get_key(a))
    en_symbol =''
    j=0
    for i in a:
        shift_j=int(shift[j])
        if ord(i) >= 97 and ord(i) <= 122:
            x = 122 - ord(i)
            if x < shift_j:
                n = 96 + (shift_j - x)
            else:
                n = ord(i) + shift_j
        elif ord(i) >= 65 and ord(i) <= 90:
            x = 90 - ord(i)
            if x < shift_j:
                n = 64 + (shift_j - x)
            else:
                n = ord(i) + shift_j
        elif ord(i) == 32:
            n = 32
        else:
            en_symbol = 'Строка содержир недопустимые символы!'
            break
        en_symbol += chr(n)
    return en_symbol

def decrypt(message):
    a = message.text
    shift = str(get_key(a))
    en_symbol = ''
    j=0
    for i in a:
        shift_j = int(shift[j])
        if ord(i) >= 97 and ord(i) <= 122:
            x = ord(i)-97
            if x < shift_j:
                n = 123 - (shift_j - x)
            else:
                n = ord(i) - shift_j
        elif ord(i) >= 65 and ord(i) <= 90:
            x = ord(i)-65
            if x < shift_j:
                n = 91 - (shift_j - x)
            else:
                n = ord(i) - shift_j
        elif ord(i)==32:
            n=32
        else:
            en_symbol = 'Строка содержир недопустимые символы!'
            break
        en_symbol += chr(n)
    return en_symbol