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
Принимаемые параметры:\nИмя, Фамилия\n
/all_users - все участники\n
/new_debt - добавление новой записи\n
Принимаемые параметры:\nИмя, Фамилия должника,
Имя, Фамилия занимающего, задолженность\n
/all_debts - все участники, которым должен выбранный\n
Принимаемые параметры:\nИмя, Фамилия\n
/all_undebts - все участники, которые должны выбранному\n
Принимаемы параметры:\nИмя, Фамилия\n
/ask_debt - задолженность между двумя выбранными участниками\n
Принимаемые параметры:\nИмя, Фамилия первого участника,\n
Имя, Фамилия второго участника\n
'''


class User:
    def __init__(self, user_id):
        self.id = user_id
        self.action = 'start'


@bot.message_handler(command='new_user')
def new_user(message):
    result = bot_commands.add_user(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(command='all_users')
def all_users(message):
    result = bot_commands.all_users()
    bot.send_message(message.chat.id, result)


@bot.message_handler(command='new_debt')
def new_debt(message):
    result = bot_commands.update_debt(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(command='all_debts')
def get_all_debts(message):
    result = bot_commands.get_all_debts(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(command='all_undebts')
def get_all_undebts(message):
    result = bot_commands.get_all_undebts(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(command='ask_debt')
def get_all_undebts(message):
    result = bot_commands.ask_debt(message.text)
    bot.send_message(message.chat.id, result)

if __name__ == '__main__':
    bot.polling(none_stop=True)
