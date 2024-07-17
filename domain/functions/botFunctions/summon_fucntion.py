import time
import telebot
from telebot.types import User

# Переменная для отслеживания времени последнего вызова команды
last_summon_time = 0

# Задержка между вызовами команды (5 минут = 300 секунд)
cooldown_period = 300

def get_chat_members(bot, chat_id):
    try:
        # Получаем список участников чата
        members = []
        for member in bot.get_chat_administrators(chat_id):
            # Добавляем только активных пользователей (не ботов)
            if not member.user.is_bot:
                members.append(member.user)
        return members
    except Exception as e:
        print(f'Ошибка при получении информации о члене чата: {e}')
        return None

def summon_all_members(bot, message):
    global last_summon_time

    # Получаем текущее время
    current_time = time.time()

    # Проверяем, прошло ли достаточно времени с момента последнего вызова команды
    if current_time - last_summon_time < cooldown_period:
        # Вычисляем оставшееся время до окончания задержки
        remaining_time = int(cooldown_period - (current_time - last_summon_time))
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        bot.send_message(message.chat.id, f'Подождите ещё {minutes} минут и {seconds} секунд перед вызовом всех участников')
        return f'Подождите ещё {minutes} минут и {seconds} секунд перед вызовом всех участников', False

    # Обновляем время последнего вызова команды
    last_summon_time = current_time

    # Получаем ID чата
    chat_id = message.chat.id

    try:
        # Получаем список участников чата
        members = get_chat_members(bot, chat_id)

        if members is None:
            return 'Произошла ошибка при получении информации о члене чата. Попробуйте позже.', False

        # Формируем текст для упоминания всех участников
        mention_text = 'Внимание, все участники чата!\n'
        for member in members:
            # Проверяем, есть ли у пользователя юзернейм
            if member.username:
                mention_text += f"@{member.username} "
            else:
                mention_text += f'<a href="tg://user?id={member.id}">{member.first_name}</a> '

        # Отправляем сообщение с упоминаниями всех участников
        bot.send_message(chat_id, mention_text, parse_mode="html")

        # Возвращаем None (без ошибки) и флаг успеха True
        return None, True

    except Exception as e:
        # Обработка других ошибок
        print(f'Произошла ошибка: {e}')
        return 'Произошла ошибка при вызове всех участников чата. Попробуйте позже.', False
