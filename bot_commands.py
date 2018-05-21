import db
import db_query
import re

many_arguments = 'Слишком мало аргументов'
less_arguments = 'Недостаточно аргументов'
wrong_arguments = 'Введены некорректные данные'


def add_user(name, surname):
    return(db_query.add_user(name, surname))


def all_users():
    names, surnames = db_query.all_users()
    if len(names) == 0:
        return('Ни один пользователь еще не добавлен')
    result = ''
    for i in range(len(names)):
        result += '{}. '.format(i + 1) + names[i] + ' ' + surnames[i] + '/n'
    return result


def get_all_debts(message_text):
    text = re.findall(r'\w+', message_text)
    if len(text) > 2:
        return many_arguments
    if len(text) < 2:
        return less_arguments
    if(''.join(text).is_alpha()):
        humans, value = db_query.get_all_debts(text[0], text[1])
        result = ''
        cur = 0
        for human in humans:
            reault += '{}. {} {} - {}'.format(cur + 1, human[0],
                                              human[1], debt[cur]) + '/n'
            cur += 1
        return result
    else:
        return wrong_arguments


def get_all_undebts(message_text):
    text = re.findall(r'\w+', message_text)
    if len(text) > 2:
        return many_arguments
    if len(text) < 2:
        return less_arguments
    if(''.join(text).is_alpha()):
        humans, value = db_query.get_all_undebts(text[0], text[1])
        result = ''
        cur = 0
        for human in humans:
            reault += '{}. {} {} - {}'.format(cur + 1, human[0], human[1],
                                              debt[cur]) + '/n'
            cur += 1
        return result
    else:
        return wrong_arguments


def debt(message_text):
    text = re.findall(r'\w+', message_text)
    if(len(text) < 5):
        return less_arguments
    if(len(text) > 5):
        return many_arguments
    if(''.join(text[:4]).is_alpha() and text[-1].is_digit()):
        result = update_debt(text[0], text[1], text[2], text[3], text[4])
        return result
    else:
        return wrong_arguments
    # users = db_query.create_debt(from_name,\
    #  from_surname, to_name, to_surname, value)
