import telebot
import bot_commands
import re


COMMAND_LIST = ['start', 'help', 'new_user',
                'all_users', 'new_debt', 'all_debts', 'all_undebts']
# Список команд, принимаемых ботом
GREETING = '''Приветствую! Я бот, который поможет Вам следить за задолженностями между Вами и вашими друзьями.
            Чтобы прочесть список команд, введите /help'''
# Приветствие при начале использования бота
HELP_LIST = '''/help - список команд
/start - начало общения с ботом
/new_user - добавление нового участника
Принимаемые параметры:
Имя, Фамилия
/all_users - все участники
/new_debt - добавление новой записи
Принимаемые параметры:
Имя, Фамилия должника, Имя, Фамилия занимающего, задолженность
/all_debts - все участники, которым должен выбранный
Принимаемые параметры:
Имя, Фамилия
/all_undebts - все участники, которые должны выбранному
Принимаемы параметры:
Имя, Фамилия
/ask_debt - задолженность между двумя выбранными участниками
Принимаемые параметры:
Имя, Фамилия первого участника, Имя, Фамилия второго участника
'''


with open('TOKEN.txt', 'r') as file:
    TOKEN = file.read().strip()
bot = telebot.TeleBot(TOKEN) 


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.action = 'start'


@bot.message_handler(commands=['help', 'start'])
def bot_help(message):
    bot.send_message(message.chat.id, HELP_LIST)


@bot.message_handler(commands=['new_user'])
def new_user(message):
    # result = bot_commands.add_user(message.text, message.chat.id)
    bot.send_message(message.chat.id)


@bot.message_handler(commands=['all_users'])
def all_users(message):
    result = bot_commands.all_users(message.chat.id)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['new_debt'])
def new_debt(message):
    result = bot_commands.update_debt(message.text, message.chat.id)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['all_debts'])
def get_all_debts(message):
    result = bot_commands.get_all_debts(message.text, message.chat.id)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['all_undebts'])
def get_all_undebts(message):
    result = bot_commands.get_all_undebts(message.text, message.chat.id)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['ask_debt'])
def ask_debt(message):
    result = bot_commands.ask_debt(message.text, message.chat.id)
    bot.send_message(message.chat.id, result)


@bot.message_handler()
def wrong_message(message):
    bot.send_message(message.chat.id, 'Неверно введена команда.\nВоспользуйтесь /help для получения списка доступных команд.')


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except RuntimeError:
            pass
