import os
import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

from utils import dialogflow_reply


def reply_to_message(event, vk_api, project_id):
    reply = dialogflow_reply(event.text, project_id)
    if reply:
        vk_api.messages.send(
            user_id=event.user_id,
            message=reply,
            random_id=random.randint(1, 1000)
        )


def main():
    load_dotenv()
    project_id = os.environ.get("PROJECT_ID")
    vk_session = vk.VkApi(token=os.environ.get("VK_TOKEN"))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_to_message(event, vk_api, project_id)


if __name__ == '__main__':
    main()
