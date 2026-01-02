import os

from dotenv import load_dotenv
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from google.cloud import dialogflow


def start(update, context):
    update.message.reply_text('Здравствуйте')


def dialogflow_reply(message):
    project_id = os.getenv('PROJECT_ID')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, "1")

    text_input = dialogflow.TextInput(text=message, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

    return response.query_result.fulfillment_text


def reply_to_message(update, context):
    reply = dialogflow_reply(update.message.text)
    update.message.reply_text(reply)


def main():
    load_dotenv()
    tg_token = os.getenv('TG_TOKEN')
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text, reply_to_message))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
