from bs4 import BeautifulSoup
import requests


def get_anecdote(bot, message):
    chat_id = message.chat.id
    url = 'https://anekdoty.ru/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')
    article = soup.find(name="div", class_="holder-body")
    if article:
        title = article.text.strip()
        bot.send_message(chat_id, title)
    else:
        bot.send_message(chat_id, "Анекдот не найден.")

