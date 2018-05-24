import db
import db_query
import re

many_arguments = 'Слишком много аргументов'
less_arguments = 'Недостаточно аргументов'
wrong_arguments = 'Введены некорректные данные'


def add_user(message_text, chat_id):
    text = re.findall(r'\w+', message_text)[1:]
    if len(text) > 2:
        return many_arguments
    if len(text) < 2:
        return less_arguments
    if not (''.join(text).isalpha()):
        return wrong_arguments
    return db_query.add_user(text[0], text[1], chat_id)


def all_users(chat_id):
    return db_query.all_users(chat_id)


def get_all_debts(message_text, chat_id):
    text = re.findall(r'\w+', message_text)[1:]
    if len(text) > 2:
        return many_arguments
    if len(text) < 2:
        return less_arguments
    if(''.join(text).isalpha()):
        return db_query.get_all_debts(text[0], text[1], chat_id)
    else:
        return wrong_arguments


def get_all_undebts(message_text, chat_id):
    text = re.findall(r'\w+', message_text)[1:]
    if len(text) > 2:
        return many_arguments
    if len(text) < 2:
        return less_arguments
    if(''.join(text).isalpha()):
        return db_query.get_all_undebts(text[0], text[1], chat_id)
    else:
        return wrong_arguments


def ask_debt(message_text, chat_id):
    text = re.findall(r'\w+', message_text)[1:]
    if len(text) > 4:
        return many_arguments
    if len(text) < 4:
        return less_arguments
    if(''.join(text).isalpha()):
        return db_query.select_debt(text[0], text[1], text[2], text[3], chat_id)
    else:
        return wrong_arguments


def update_debt(message_text, chat_id):
    text = re.findall(r'\w+', message_text)[1:]
    if(len(text) < 5):
        return less_arguments
    if(len(text) > 5):
        return many_arguments
    sign = 1
    if message_text[message_text.find(text[-1]) - 1] in ('-', '−'):
        sign = -1
    if(''.join(text[:4]).isalpha() and text[-1].isdigit()):
        result = db_query.update_debt(
            text[0], text[1], text[2], text[3], sign * int(text[4]), chat_id)
        return result
    else:
        return wrong_arguments
