from typing import List

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import  ListTrainer
from flask import Flask, render_template, request


app = Flask(__name__)
myBot = ChatBot(
    "MyBot",
    logic_adapters=[
        {
            'import_path': 'bot_internaladapter.InternalAdapter'
        }

    ])

# myBot = ChatBot(
#     "MyBot",
#     logic_adapters=[
#         {
#             'import_path': 'bot_internaladapter.InternalAdapter'
#         },
#         {
#             'import_path': 'chatterbot.logic.BestMatch'
#
#         },
#         {
#             'import_path': 'chatterbot.logic.MathematicalEvaluation'
#         }
#
#     ])

trainer = ChatterBotCorpusTrainer(myBot)
trainer.train("chatterbot.corpus.english")
trainer.train("chatterbot.corpus.english.greetings")
trainer.train("chatterbot.corpus.english.conversations")
trainer_list = ListTrainer(myBot)


data = open('chats', 'r').readlines()
conv = []
for i in data:
    conv.append(i.strip('\n'))
trainer_list.train(conv)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(myBot.get_response(userText))


if __name__ == '__main__':
    app.run()
