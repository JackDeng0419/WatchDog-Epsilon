import time
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests


app = Flask(__name__)
CORS(app)

user_id = ''

@app.route('/post_test', methods=['POST'])
def post_test():
    global user_id
    user_id = request.json['userId']
    print(f"user_id: {user_id}")
    return jsonify({"status": "success"}), 200

@app.route('/a', methods=['GET'])
def test():
    global user_id
    headers = {
        "Authorization": "Basic " + "NDgxNDA5ZjQtZWYyOC00ZTgxLWI4ZTMtMzFlYjFmMjM2NTYx",
        "Content-Type": "application/json"
    }

    payload = {
        "app_id": "559429a4-ed04-4886-83b0-ee8ae5197c5d",
        "include_player_ids": [user_id],
        "existing_android_channel_id": "86d08287-104c-40a2-86c8-d8ed748c6962",
        "contents": {"en": "11111"},
        "headings": {"en": "Message at" + str(datetime.now())}
    }

    print(payload)
    response = requests.post("https://onesignal.com/api/v1/notifications", json=payload, headers=headers)

    print(response)
    return jsonify(response.json()), response.status_code

if __name__ == "__main__":
    app.run(debug=True, port=5000)
