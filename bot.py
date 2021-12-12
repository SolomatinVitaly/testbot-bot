from config import TOKEN
from telebot import TeleBot
from handler import Handler


bot = TeleBot("5050018090:AAGyqAS5hF4CK7mP3q2QT-w9td55kuEafAM")
handler = Handler()


@bot.message_handler()
def answer(message):
    bot.send_message(
        message.chat.id,
        handler.get_response(message.chat.id, message.text)
    )


if __name__ == '__main__':
    bot.polling(none_stop=True)
