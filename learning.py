import argparse
import json
import os

from google.cloud import dialogflow
from dotenv import load_dotenv


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


def main():
    parser = argparse.ArgumentParser(
        description="Скрипт для тренировки бота по тренировочным фразам"
    )
    parser.add_argument(
        '-p', '--path',
        help="Путь до файла с тренировочными фразами",
        default="./questions.json"
    )
    args = parser.parse_args()

    load_dotenv()
    project_id = os.getenv('PROJECT_ID')

    path = args.path
    with open(path, 'r', encoding="UTF-8") as file:
        content_json = file.read()

    intents = json.loads(content_json)

    for intent, phrases in intents.items():
        create_intent(
            project_id,
            intent,
            phrases["questions"],
            [phrases["answer"]]
        )


if __name__ == '__main__':
    main()
