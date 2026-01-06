import os
from functools import partial

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

from utils import dialogflow_reply


def start(update, context):
    update.message.reply_text('Здравствуйте')


def reply_to_message(update, context, project_id):
    chat_id = update.effective_chat.id
    reply = dialogflow_reply(update.message.text, project_id, chat_id)
    if reply:
        update.message.reply_text(reply)


def main():
    load_dotenv()
    project_id = os.environ['PROJECT_ID']
    tg_token = os.environ['TG_TOKEN']
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    reply_to_message_with_projid = partial(reply_to_message, project_id=project_id)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, reply_to_message_with_projid))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
