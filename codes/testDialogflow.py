import json
import os
import dialogflow_v2 as dialogflow
from flask import Flask,request,jsonify

import argparse
import uuid
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='acquired-ripple-285306-8da5f9a63c48.json'

from google.protobuf.json_format import MessageToJson

# [START dialogflow_detect_intent_text]
def detect_intent_texts(text,language):
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    project_id="acquired-ripple-285306"
    session_id="session01"
    #session_id="projects/acquired-ripple-285306/agent/sessions/22976af6-873e-2f74-ac90-bdbbcfbe6815"
    language_code=language
    
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    intents=['definition', 'cons','contrast','example','pros']
    print('Session path: {}\n'.format(session))
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
          session=session, query_input=query_input)
    
    res=MessageToJson(response)
    res=json.loads(res)
    print(res)
    intent=res['queryResult']['intent']['displayName']
    if intent not in intents:
        res=res['queryResult']['fulfillmentText']
    else:
        os_norm=res['queryResult']['parameters']['os_norm']
        res=customanswer(intent,os_norm)
#    param=res['queryResult']['parameters']['os_norm']
#    print(param)
    print(res)
    print(type(res))
    return res

def definition(input_os_norm):
    os_norm=''.join(input_os_norm.split())
    with open("definition.json","r") as f:
        definition_dict=json.load(f)
    try:    
        answer=definition_dict[os_norm]
    except KeyError:
        answer="답을 구할 수 없습니다."
    
    return answer

def customanswer(intent,input_os_norm):
    if intent=="contrast":
        temp=""
        for norm in input_os_norm:
            norm=''.join(norm.split())
            temp+=norm
        os_norm=temp
    else:
        os_norm=''.join(input_os_norm.split())
    with open("../data/%s.json"%(intent),"r") as f:
        intentdict=json.load(f)
    print("customanswer intent",intent,"os_norm",os_norm)
    
    
        
    try:    
        answer=intentdict[os_norm]
    except KeyError:
        for key in intentdict.keys():
            if os_norm in key:
                answer=intentdict[key]
                break
        answer="답을 구할 수 없습니다."
    
    return answer


