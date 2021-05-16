from flask import Flask, request, Response, render_template
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
            f.close()
        return Response(status=200)
    except Exception as e:
        raise e

@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html')

@app.route('/webhook', methods=['GET'])
def get_page():
    return render_template('no.html')