from flask import Flask, request, Response, render_template
import json
import time

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def respond():
    try:
        with open('buffer.json', 'w+') as file:
            try:
                old_file = json.load(file)
                old_time = old_file['time'] 
            except Exception as e:
                print(e)
                old_time = 0

            new_json = request.json
            new_json['old_time'] = old_time
            new_json['time'] = time.time()

            json.dump(new_json, file, indent = 4)
            file.close()

            return Response(status=200)

    except Exception as e:
        raise e

@app.route('/', methods=['GET'])
def main_page():
    return render_template('index.html')

@app.route('/webhook', methods=['GET'])
def get_page():
    return render_template('no.html')