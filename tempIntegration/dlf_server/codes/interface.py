import socketserver
import socket
import threading
import json
import time
import random
import os
#import data
import sys
#import model as ml
import aiml
import csv
import pickle
#from configs import DEFINES
#from common import *
from testDialogflow import *
from konlpy.tag import Okt


IP = "114.70.21.89"
PORT = 9005
#KEY = urandom()
NAME = "AIML_CHATBOT_1"
BROKER_ADDR = ("114.70.21.89", 8000)
okt = Okt()

class ServerThread(threading.Thread):
    def __init__(self, server):
        super(ServerThread, self).__init__()
        self.server = server

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

class Chatbot():
    
    class Handler(socketserver.StreamRequestHandler):
        def handle(self):
            # message parsing
            message = self.rfile.readline().strip()
            message = message.decode("utf-8")
            print("msg:"+message)
            message = json.loads(message)
            #print((message['contents']))
            # message processing...
            data = {}
            data['contents'] = message

            # ========== intercept by input data prefix'>'
            if len(data['contents'])>0 and data['contents'][0]=='>':
                answer = ""
                print(data['contents'][1:])
                dict_data = data['contents'][1:]
                fr = open('./script/script_word.pickle','rb')
                loaded = pickle.load(fr)
                if dict_data in loaded:
                    answer = answer + '>'
                    for ts in loaded[str(dict_data)]:
                        answer = answer+str(ts)+" "
                    print(answer)
                else:
                    answer = "key: " + str(dict_data)+" is not existed"
                    print(answer)
            else:
                kern = aiml.Kernel()

                brainLoaded = False
                forceReload = False
                while not brainLoaded:
                    if forceReload or (len(sys.argv) >= 2 and sys.argv[1] == "reload"):
                        kern.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
                        brainLoaded = True
                        # kern.saveBrain("standard.brn")
                    else:
                        try:
                            kern.bootstrap(brainFile = "standard.brn")
                            brainLoaded = True
                        except:
                            forceReload = True

                # Enter the main input/output loop.
                # print("\nINTERACTIVE MODE (ctrl-c to exit)")
                
                # ============ AIML ===============
                s = data["contents"]
                res = okt.pos(s)
                content = ""
                for word in res:
                    if (word[1] == "Josa"):
                        content = content + " "+word[0]+" "
                    else:
                        content = content+ word[0]
                response = kern.respond(content)
                print("tokenized : ",response)
                if response == "해당되는 내용이 없습니다.":
                    response = kern.respond(data["contents"])
                print("row or tokenized : ",response)

                # ============ DIALOGFLOW ===============            
                if response == "해당되는 내용이 없습니다.":
                    language = "ko"
                    msg = data["contents"]
                    response = detect_intent_texts(msg,language)
                    
                answer = response
   
            # creating response message...
            self.wfile.write(answer.encode("utf-8"))
            
    def __init__(self):
        print("Chatbot creating...")
        main_srv = socketserver.ThreadingTCPServer(("", PORT), Chatbot.Handler, bind_and_activate=False)
        main_srv.allow_reuse_address = True
        main_srv.server_bind()
        main_srv.server_activate()
        self.srv_thread = ServerThread(main_srv)
        
    def start(self):
        print("Chatbot registering...")
        #self.register()
        
        print("Chatbot running...")
        self.srv_thread.start()
        
    def stop(self):
        print("Chatbot deregistering...")
        #self.deregister()
        
        print("Chatbot stopping...")
        self.srv_thread.stop()        
        self.srv_thread.join()
        
    # def register(self):
    #     data = { "key" : KEY, "addr" : (IP,PORT), "name" : "chatbot3"}
    #     sendRequest("/register?", data, BROKER_ADDR)
    
    # def deregister(self):
    #     data = { "key" : KEY }
    #     sendRequest("/deregister?", data, BROKER_ADDR)
            
if __name__ == "__main__":
    try:
        chatbot = Chatbot()
        chatbot.start()
        while True:
            time.sleep(10)            
    
    except KeyboardInterrupt:
        chatbot.stop()
        print("Clean up chatbot!")
