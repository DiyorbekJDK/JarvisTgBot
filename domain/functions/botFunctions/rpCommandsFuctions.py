import json
import os
from data.util.paths import rpCommandsFile_path

RP_COMMANDS_FILE = rpCommandsFile_path

# Функция для загрузки команд из файла
def load_rp_commands():
    if os.path.exists(RP_COMMANDS_FILE):
        with open(RP_COMMANDS_FILE, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
                else:
                    return {}
            except json.JSONDecodeError:
                return {}
    return {}

# Функция для сохранения команд в файл
def save_rp_commands(rp_commands):
    with open(RP_COMMANDS_FILE, 'w', encoding='utf-8') as file:
        json.dump(rp_commands, file, ensure_ascii=False, indent=4)

# Функция для добавления новой RP команды
def add_rp_command(bot, message, rp_commands):
    msg = bot.send_message(message.chat.id, "Введите название новой RP команды:")
    bot.register_next_step_handler(msg, process_command_name, bot, rp_commands)

def process_command_name(message, bot, rp_commands):
    command_name = message.text.lower()  # сохраним команду в нижнем регистре для консистентности
    msg = bot.send_message(message.chat.id, f"Введите текст для команды '{command_name}':")
    bot.register_next_step_handler(msg, process_command_text, bot, rp_commands, command_name)

def process_command_text(message, bot, rp_commands, command_name):
    command_text = message.text
    msg = bot.send_message(message.chat.id, f"Введите эмодзи для команды '{command_name}':")
    bot.register_next_step_handler(msg, process_command_emoji, bot, rp_commands, command_name, command_text)

def process_command_emoji(message, bot, rp_commands, command_name, command_text):
    emoji = message.text  # предполагаем, что эмодзи передается как текст
    rp_commands[command_name] = {'text': command_text, 'emoji': emoji}
    save_rp_commands(rp_commands)
    bot.send_message(message.chat.id, f"Команда '{command_name}' добавлена успешно!")

# Функция для выполнения RP команд
def make_rp_command(bot, message, rp_commands):
    chat_id = message.chat.id
    user1 = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
    user2 = f'<a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a>'
    commm = message.text.lower()

    if commm in rp_commands:
        txtToDO = rp_commands[commm]['text']
        emoji = rp_commands[commm]['emoji']
        bot.send_message(chat_id=chat_id, text=f'{emoji} | {user1} {txtToDO} {user2}',
                         reply_to_message_id=message.reply_to_message.message_id, parse_mode="html")
