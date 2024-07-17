##################################
# Main code file, were bots work #
##################################

from domain.functions.botFunctions.botMainFunctions import *
from domain.functions.dbFunctions.databaseFunctions import *
from data.util.tokens import bot_token
from data.util.lists import *
import random
from domain.functions.botFunctions.rpCommandsFuctions import *
from domain.functions.botFunctions.summon_fucntion import *

bot = telebot.TeleBot(bot_token)


def allCode():
    # Загрузка команд при запуске бота
    rp_commands = load_rp_commands()
    if not isinstance(rp_commands, dict):
        rp_commands = {}

    @bot.message_handler(commands=['start'])
    def start(message):
        if message.chat.type == "private":
            user_id = message.from_user.id
            if not isUserInDb(user_id):
                saveUser(user_id, message.from_user.username)
                reply_message(message, "Чем помочь сэр?")
            else:
                reply_message(message, "Чем помочь сэр?")
        elif message.chat.type == "supergroup" or "group":
            group_id = message.chat.id
            if not isGroupInDb(group_id):
                saveGroup(group_id, message.chat.username)
                reply_message(message, "Чем помочь сэр?")
            else:
                reply_message(message, "Чем помочь сэр?")

    # Обработчик команды для добавления новой RP команды
    @bot.message_handler(commands=['add_rp'])
    def handle_add_rp_command(message):
        add_rp_command(bot, message, rp_commands)

    # Обработчик сообщений для выполнения RP команд
    @bot.message_handler(func=lambda message: message.reply_to_message)
    def handle_make_rp_command(message):
        make_rp_command(bot, message, rp_commands)

    @bot.message_handler()
    def messages_from_users(message):
        text = message.text.lower()
        chat_id = message.chat.id
        if text in jarvis_names:
            word = random.choice(jarvis_answers_to_call).capitalize()
            reply_message(message, word)
        elif text == "бот":
            send_message(chat_id,"на месте✅")
        elif text == "пин":
            reply_message(message,"понг")
        elif text == "собрать всех":
            summon_all_members(bot,message)

    bot.polling(none_stop=True)
