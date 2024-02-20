import re


user_states = {}


def is_calc_mode(chat_id):
    return user_states.get(chat_id, False)


def activate_calc_mode(bot, message):
    chat_id = message.chat.id
    user_states[chat_id] = True
    bot.reply_to(message, "Калькулятор активирован. \nВведите выражение для расчета. Например, 2+2")


def calc(bot, message):
    chat_id = message.chat.id
    expression = message.text


    if re.match(r'^[\d\+\-\*\/\(\)\s\.]+$', expression):
        try:
            result = eval(expression)
            bot.send_message(chat_id, "Результат: " + str(result))
        except Exception as e:
            bot.send_message(chat_id, "Ошибка: неверное выражение")
    elif message.text == "stop":
        user_states[chat_id] = False
        bot.reply_to(message, "Калькулятор деактивирован.")
    else:
        bot.send_message(chat_id, "Пожалуйста, введите математическое выражение")


