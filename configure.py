from flask import Flask, request, jsonify, render_template, send_from_directory
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('configure.html')


@app.route('/configure', methods=['POST'])
def configure():
    data = request.json
    print(data['data'])
    with open('config.json', 'w') as f:
        json.dump(data, f)
    return jsonify(data)

@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('assets/configurator', filename)


if __name__ == '__main__':
    app.run(debug=True)