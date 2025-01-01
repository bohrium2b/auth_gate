from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('configure.html')


@app.route('/configure', methods=['POST'])
def configure():
    data = request.post['data']
    with open('config.json', 'w') as f:
        json.dump(data, f)
    return jsonify(data)

