import json
import os
import dialogflow_v2 as dialogflow
import pandas as pd
from testDialogflow import *
project_id="acquired-ripple-285306"
session_id="session01"
#session_id="projects/acquired-ripple-285306/agent/sessions/22976af6-873e-2f74-ac90-bdbbcfbe6815"
language_code="ko"

def detect_intent(question):
    
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    
    text_input = dialogflow.types.TextInput(text=question, language_code=language_code)
    
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = session_client.detect_intent(
          session=session, query_input=query_input)

    res=MessageToJson(response)
    res=json.loads(res)
    
    try:
        intent=res['queryResult']['intent']['displayName']
        os_norm=res['queryResult']['parameters']['os_norm']
        os_norm_str=''.join(os_norm)
        print("%s - %s"%(intent,os_norm_str))
        
        if intent =="contrast" and len(os_norm)>1:
            os_norm_str2=os_norm[1]+os_norm[0] 
        else:
            os_norm_str2=""
        
    except KeyError:
        print("error in ",question)
        os_norm_str=question
        os_norm_str2=""
        
    return intent,os_norm_str,os_norm_str2

def generate_qnaset(filepath_toload="../data/os_qna.csv",filepath_tosave="../data/"):
    qna_df=pd.read_csv(filepath_toload)
    questions=qna_df['Question'].tolist()
    answers=qna_df['Answer'].tolist()
    
    intents=['pros', 'definition', 'contrast', 'example', 'cons','Default Fallback Intent','feature']
    dataset=[]
    for intentlist in range(len(intents)):
        dataset.append(dict())

    qna_dataset=dict(zip(intents,dataset))

    for question,answer in zip(questions,answers):
        print(question)
        if type(question) is float:
            continue
        intent,osnorm,osnorm2=detect_intent(question)
        qna_dataset[intent][osnorm]=answer
        if len(osnorm2)>0:
            qna_dataset[intent][osnorm2]=answer
    for intent in intents:
        if len(qna_dataset[intent])==0:
            continue
        else:
            filepath_tosave+="/" if filepath_tosave[-1] !="/" else ""
            with open("%s%s.json"%(filepath_tosave,intent), "w", encoding='utf8') as outfile:  
                json.dump(qna_dataset[intent], outfile, ensure_ascii=False)

if __name__ == "__main__":
    generate_qnaset()
