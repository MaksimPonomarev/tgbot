import sqlite3
from config import bot


def add_user_to_db(user_id):
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE)")
        try:
            cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            conn.commit()

        except sqlite3.IntegrityError:
            print(f"Пользователь с ID {user_id} уже существует.")


def get_all_user_ids():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        user_ids = [row[0] for row in cursor.fetchall()]
        print("Зарегистрированные ID пользователей:")
        for user_id in user_ids:
            print(user_id)
        return user_ids


def send_daily_reminder():
    user_ids = get_all_user_ids()
    for user_id in user_ids:
        try:
            bot.send_message(user_id, "")
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


if __name__ == '__main__':
    send_daily_reminder()