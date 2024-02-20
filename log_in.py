import bcrypt
import sqlite3
from config import bot


def start_login(bot, message):

    msg = bot.send_message(message.chat.id, "Введите ваше имя (логин)")
    bot.register_next_step_handler(msg, get_name)


def get_name(message):
    chat_id = message.chat.id
    user_name = message.text
    msg = bot.send_message(chat_id, "Введите ваш пароль")
    bot.register_next_step_handler(msg, lambda m: process_login_step(m, user_name))

def process_login_step(message, user_name):
    user_password = message.text.encode('utf-8')

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT hash_password FROM test_users WHERE name = ?", (user_name,))
    user_record = cursor.fetchone()

    if user_record:
        stored_hash_password = user_record[0]

        if bcrypt.checkpw(user_password, stored_hash_password):
            bot.send_message(message.chat.id, "Вы успешно вошли в систему!")
        else:
            bot.send_message(message.chat.id, "Неправильный пароль. Попробуйте ещё раз.")
    else:
        bot.send_message(message.chat.id, "Пользователь с таким именем не найден.")

    conn.close()