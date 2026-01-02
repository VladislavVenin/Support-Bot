import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters


def start(update, context):
    update.message.reply_text('Здравствуйте')


def echo(update, context):
    update.message.reply_text(update.message.text)


def main():
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
