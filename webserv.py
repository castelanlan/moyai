from flask import Flask, request, Response
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    try:
        with open('buffer.json', 'w') as f:
            json.dump(request.json, f, indent = 4)
        return Response(status=200)
    except Exception as e:
        raise e