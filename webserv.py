from flask import Flask, request, Response
import json
import time

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    new_json = request.json
    new_json['time'] = time.time()
    print(new_json)
    try:
        with open('buffer.json', 'w+') as f:
            json.dump(new_json, f, indent = 4)
        return Response(status=200)
    except Exception as e:
        raise e