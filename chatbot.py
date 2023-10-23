import bardapi
import os
from flask import Flask, request, jsonify
import google.cloud.dialogflow_v2 as dialogflow

# global varibles
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path-google-service-account"
project_id = "project-id"
session_id = "session-id "


app = Flask(__name__) 

# an endpoint to call bard this could be used if needed for more general IT stuff
@app.route('/get_AI_response_bard/<user_input>')
def get_AI_response_bard(user_input): 
        
    bard = bardapi.Bard(token=("bard-api-key"))
    response = bard.get_answer(str(user_input))
    
    return jsonify(response), 200

#get the response form the agent
@app.route('/', methods=["POST", "GET"])
def get_AI_response_dialogflow(): 

    if request.method == "GET": 
        print('here')        
        return "called GET", 200

    if request.method == "POST": 
        payload = request.json
        
        print(payload)
        
        user_response = (payload['queryResult']['queryText'])
        bot_response = (payload['queryResult']['fulfillmentText'])
        
        print(bot_response)
        
        return jsonify(bot_response),200
        
    else: 
        response = "hello world"
        return jsonify(response), 200
    
#posting to reposne to agent
@app.route('/GetAgentResponse/<user_input>')
def post_to_dialog_flow(user_input): 
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, "session-id")

    text_input = dialogflow.types.TextInput(text=user_input, language_code="EN")
    query_input = dialogflow.types.QueryInput(text=text_input)
    response_dialogflow = session_client.detect_intent(session=session, query_input=query_input)
    
    try:
        bot_response = response_dialogflow.query_result.fulfillment_text
        print(bot_response)
        return bot_response, 200
    except:
        return "there has been an error",500 
        
    
if __name__ == "__main__":
    app.run(debug=False )
