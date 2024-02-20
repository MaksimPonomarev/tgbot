from calculation import activate_calc_mode, calc, is_calc_mode
from telebot import types
from config import VK, GIT, LINKEDIN, bot
from database import start_registration
from anecdot import get_anecdote
from log_in import start_login
from reminder import  add_user_to_db


@bot.message_handler(commands=['start', 'hello'])
def start(message):

    add_user_to_db(message.chat.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton('VK')
    btn2 = types.KeyboardButton('git')
    btn3 = types.KeyboardButton('calculator')
    btn4 = types.KeyboardButton('Linkedin')
    btn5 = types.KeyboardButton('registration')
    btn6 = types.KeyboardButton('anecdot')
    btn7 = types.KeyboardButton('login')
    markup.row(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}, ниже список моих умений :)", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'VK')
def open_vk(message):
    bot.send_message(message.chat.id, VK)


@bot.message_handler(func=lambda message: message.text == 'git')
def open_git(message):
    bot.send_message(message.chat.id, GIT)


@bot.message_handler(func=lambda message: message.text == 'Linkedin')
def open_linkedin(message):
    bot.send_message(message.chat.id, LINKEDIN)


@bot.message_handler(func=lambda message: message.text == 'anecdot')
def send_anec(message):
    get_anecdote(bot, message)


@bot.message_handler(func=lambda message: message.text.lower() == 'registration')
def handle_registration_command(message):
    start_registration(message)


@bot.message_handler(func=lambda message: message.text.lower() == 'login')
def handle_registration_command(message):
    start_login(bot, message)


@bot.message_handler(func=lambda message: message.text == 'calculator')
def handle_calc_command(message):
    activate_calc_mode(bot, message)


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if is_calc_mode(message.chat.id):
        calc(bot, message)




bot.polling(non_stop=True)