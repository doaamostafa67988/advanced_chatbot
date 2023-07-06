# Import liberiers
from flask import Flask, render_template,jsonify
from utils import custom_chatbot 
from utils import capture_voice
from flask import request
import random
import os

app = Flask(__name__)


@app.route('/chatbot_text', methods=['POST'])
def chatbot_response():
       message = request.json['message']
       response = str(custom_chatbot(user_prompt=message))
       #response = chatbot.get_response(message).text
       return jsonify({'response': response})


@app.route('/chatbot_voice', methods=['POST'])
def voice_talk():
            message = request.json['message']
            if message:
                destenation=capture_voice()
                response= str(custom_chatbot(destination=destenation))
                return jsonify({'response': response})
            else:
                return jsonify({'response': ''})
           

if __name__ == '__main__':
    app.run(debug=True)