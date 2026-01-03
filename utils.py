import os

from google.cloud import dialogflow


def dialogflow_reply(message):
    project_id = os.getenv('PROJECT_ID')
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, "1")

    text_input = dialogflow.TextInput(text=message, language_code="ru")
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
    if response.query_result.intent.is_fallback:
        return False
    return response.query_result.fulfillment_text
