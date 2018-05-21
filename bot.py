import telebot
import bot_commands
import re

commands_list = ['start', 'help']


# Число выводимых последних тем/статей по умолчанию
command_list = ['start', 'help', 'new_user',
                'all_users', 'new_debt', 'all_debts', 'all_undebts']
# Список команд, принимаемых ботом
greeting = '''Приветствую! Я бот, который поможет Вам\n
            следить за задолженностями между Вами и вашими друзьями.\n
            Чтобы прочесть список команд, введите /help'''
# Приветствие при начале использования бота
help_list = '''/help - список команд\n
/start - начало общения с ботом\n
/new_user - добавление нового участника\n
Принимаемые параметры: Имя, Фамилия\n
/all_users - все участники\n
/new_debt - добавление новой записи\n
Принимаемые параметры: Имя, Фамилия должника,\n
Имя, Фамилия занимающего, задолженность\n
/all_debts - все участники, которым должен выбранный\n
Принимаемые параметры: Имя, Фамилия\n
/all_undebts - все участники, которые должны выбранному
'''

users = {}
with open('TOKEN.txt', 'r') as file:
    token = file.readline()[:-1]
bot = TeleBot(token)


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.action = 'start'


@bot.message_handler(command='new_user')
def new_user(message):
    # add_user(message.chat.id)
    result = bot_commands.add_user(message.chat.first_name,
                                   message.chat.last_name)
    bot.send_message(message.chat.id, result)
    # users[message.chat.id].action = 'start'


@bot.message_handler(command='all_users')
def all_users(message):
    result = bot_commands.all_users()
    bot.send_message(message.chat.id, result)


@bot.message_handler(command='new_debt')
def new_debt(message):
    result = bot_commands.update_debt(message_text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(command='all_debts')
def get_all_debts(message):
    result = bot_commands.get_all_debts(message_text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(command='all_undebts')
def get_all_undebts(message):
    result = bot_commands.get_all_undebts(message_text)
    bot.send_message(message.chat.id, result)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except RuntimeError:
            pass
