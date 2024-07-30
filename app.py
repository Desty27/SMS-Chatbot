from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
import dialogflow_v2 as dialogflow
import os

app = Flask(__name__)


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your/dialogflow-credentials.json"

@app.route("/sms", methods=['POST'])
def sms_reply():
    
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()
    df_response = detect_intent_texts("your-dialogflow-project-id", "unique-session-id", incoming_msg, 'en-US')
    reply = df_response.query_result.fulfillment_text
    response.message(reply)
    return str(response)

def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    
    response = session_client.detect_intent(session=session, query_input=query_input)
    return response

if __name__ == "__main__":
    app.run(debug=True)
