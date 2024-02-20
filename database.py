import telebot
import sqlite3
import bcrypt
from config import bot

user_data = {}


def start_registration(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Привет, сейчас будет регистрация. Напиши свое имя")
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'name': message.text.strip()}
    bot.send_message(chat_id, "Введите пароль")
    bot.register_next_step_handler(message, user_password)


def user_password(message):
    chat_id = message.chat.id
    password = message.text.strip().encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    with sqlite3.connect("data.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_users (
                id INTEGER PRIMARY KEY, 
                name TEXT, 
                hash_password TEXT
            )
        """)
        conn.commit()

        cursor.execute("INSERT INTO test_users (name, hash_password) VALUES (?, ?)",
                       (user_data[chat_id]['name'], hashed_password))
        conn.commit()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("Список пользователей", callback_data="users"))
    bot.send_message(chat_id, "Пользователь зарегистрирован", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM test_users")
    users = cursor.fetchall()

    info = ""
    for elem in users:
        info += f"Имя: {elem[1]}, Пароль: {elem[2]}\n"

    cursor.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


