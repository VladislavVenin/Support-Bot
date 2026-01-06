import argparse
import json
import os

from google.cloud import dialogflow
from google.api_core.exceptions import InvalidArgument
from dotenv import load_dotenv


def convert_to_str(input_value):
    """Convert nonstr elements to str"""
    if type(input_value) is list:
        converted = [str(element) for element in input_value]
    else:
        converted = str(input_value)
    return converted


def add_to_list(input_value):
    """Add non list vars to list"""
    if type(input_value) is not list:
        return [input_value]
    return input_value


def create_intents_list_with_ids(project_id):
    """Create list of existing intents with ids"""
    client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    intents = client.list_intents(parent=parent)

    intents_ids = {}
    for intent in intents:
        intents_ids[f"{intent.display_name}"] = os.path.basename(intent.name)
    return intents_ids


def delete_intent(project_id, intent_id):
    """Delete intent with the given intent type and intent value."""
    intents_client = dialogflow.IntentsClient()

    intent_path = intents_client.intent_path(project_id, intent_id)

    intents_client.delete_intent(request={"name": intent_path})


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create new intent"""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)
    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def main():
    parser = argparse.ArgumentParser(
        description="Скрипт для тренировки бота по тренировочным фразам"
    )
    parser.add_argument(
        '-p', '--path',
        help="Путь до файла с тренировочными фразами",
        default="./questions.json"
    )
    parser.add_argument(
        '-r', '--rewrite',
        action="store_true",
        help="Перезаписать существующие записи",
    )
    args = parser.parse_args()

    load_dotenv()
    project_id = os.environ["PROJECT_ID"]

    path = args.path
    with open(path, 'r', encoding="UTF-8") as file:
        intents_payload = file.read()

    intents = json.loads(intents_payload)
    if args.rewrite:
        intents_ids = create_intents_list_with_ids(project_id)
    for intent, phrases in intents.items():
        questions = convert_to_str(phrases["questions"])
        answers = convert_to_str(phrases["answer"])

        questions = add_to_list(questions)
        answers = add_to_list(answers)

        try:
            create_intent(
                project_id,
                intent,
                questions,
                answers
            )
            print("Intent created: {}".format(intent))
        except InvalidArgument as e:
            if args.rewrite:
                intent_id = intents_ids.get(intent)
                delete_intent(project_id, intent_id)
                create_intent(project_id, intent, questions, answers)
                print("Intent created: {}".format(intent))
            else:
                print(e)
                continue


if __name__ == '__main__':
    main()
