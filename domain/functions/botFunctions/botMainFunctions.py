#################
# Bot functions #
#################

import telebot
from data.util.tokens import bot_token
from telebot import types
from data.util.links import *
import time
from telebot import apihelper

bot = telebot.TeleBot(bot_token)


def send_message(chat_id: int, mess: str, parseMode=''):
    bot.send_message(chat_id, mess.capitalize(), parseMode)


def reply_message(message, text: str):
    bot.reply_to(message, text)


def log(text):
    print(f"LOG: {text}")


def errorNotif(address, error_type):
    send_message(owner_id, f"ERROR|Where: {address}, text: {error_type} ")


def sendErrorMessToUser(user_id: int):
    send_message(user_id, "🤕Произошла какая-та ошибка...")




