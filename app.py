from typing import List

import flask
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import  ListTrainer
from flask import Flask, render_template, request, make_response
import nltk

# Set your proxy here if using from some proxy place
# nltk.set_proxy('http://proxy.mycompany.com:83')
app = Flask(__name__)
myBot = ChatBot(
    "MyBot",
    logic_adapters=[
        {
            'import_path': 'incidents.bot_incidentadapter.IncidentAdapter'
        },
        {
            'import_path': 'address.bot_addressadapter.BotAddressAdapter'
        },
        {
            'import_path': 'chatterbot.logic.BestMatch'

        }

    ])


trainer = ChatterBotCorpusTrainer(myBot)
trainer.train("chatterbot.corpus.english")
trainer.train("chatterbot.corpus.english.greetings")
trainer.train("chatterbot.corpus.english.conversations")

trainer_list = ListTrainer(myBot)

def trainListFromFile(filename):
    data = open(filename, 'r').readlines()
    conv = []
    for i in data:
        conv.append(i.strip('\n'))
    trainer_list.train(conv)

trainListFromFile('training-lists/incident-list.txt')
trainListFromFile('training-lists/addresschange-list.txt')
trainListFromFile('training-lists/createincident-list.txt')




@app.route("/")
def home():
    return render_template("index.html")

def setContextAndReturn(input):
    result = input
    res = make_response(result)
    if("#CONTEXT#" in input):
        dataArray = input.split("#CONTEXT#");
        result = dataArray[0];
        contextName = dataArray[1];
        res = make_response(result)
        res.set_cookie('context', contextName, max_age=60 * 60 * 24 * 365 * 2)
    return res;




@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    result = str(myBot.get_response(userText))
    res = setContextAndReturn(result)
    return res


if __name__ == '__main__':
    app.run()
