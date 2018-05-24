import telebot
import bot_commands
import re


COMMAND_LIST = ['start', 'help', 'new_user',
                'all_users', 'new_debt', 'all_debts', 'all_undebts']
# Список команд, принимаемых ботом
GREETING = '''Приветствую! Я бот, который поможет Вам\n
            следить за задолженностями между Вами и вашими друзьями.\n
            Чтобы прочесть список команд, введите /help'''
# Приветствие при начале использования бота
HELP_LIST = '''/help - список команд\n
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


cur_chat_id = 0


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


@bot.message_handler(commands='new_user')
def new_user(message):
    bot_commands.check_chat_id(message.chat.id)
    chat_id = message.chat.id
    result = bot_commands.add_user(message.text, chat_id)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands='all_users')
def all_users(message):
    bot_commands.check_chat_id(message.chat.id)
    result = bot_commands.all_users()
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands='new_debt')
def new_debt(message):
    bot_commands.check_chat_id(message.chat.id)
    result = bot_commands.update_debt(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands='all_debts')
def get_all_debts(message):
    bot_commands.check_chat_id(message.chat.id)
    result = bot_commands.get_all_debts(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands='all_undebts')
def get_all_undebts(message):
    bot_commands.check_chat_id(message.chat.id)
    result = bot_commands.get_all_undebts(message.text)
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands='ask_debt')
def get_all_undebts(message):
    bot_commands.check_chat_id(message.chat.id)
    result = bot_commands.ask_debt(message.text)
    bot.send_message(message.chat.id, result)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except RuntimeError:
            pass
