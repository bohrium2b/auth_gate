from flask import Flask, request, jsonify, render_template
import json
from argparse import ArgumentParser

arg_parser = ArgumentParser()
arg_parser.add_argument('--port', type=int, default=5000)
arg_parser.add_argument('config', type=str)
args = arg_parser.parse_args()

with open(args.config, 'r') as f:
    config = json.load(f)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

