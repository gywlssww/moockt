from flask import Flask,request, render_template,jsonify
import datetime
import json
from testDialogflow import *

app = Flask(__name__)
app.config['JSON_AS_ASCII']=False
@app.route("/")
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    result="not yet"
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'result':result
    }
    return render_template('main.html', **templateData)
@app.route("/definition",methods=['POST'])
def definition():
    return "defition"

@app.route("/message",methods=['POST'])
def message():
    req=request.get_json()
    msg=req['userRequest']['utterance']
    language="ko"
    ret={
            "version":"2.0",
            "template":{
                "outputs":[
                    {
                        "simpleText":{
                            "text":detect_intent_texts(msg,language)
                            }
                        }
                    ]
                }
    }

    return ret

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)


