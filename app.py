import requests
from flask import Flask, request, jsonify, render_template, redirect
import json
from oauthlib.oauth2 import WebApplicationClient
from argparse import ArgumentParser
import os 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

arg_parser = ArgumentParser()
arg_parser.add_argument('--port', type=int, default=5000)
arg_parser.add_argument('config', type=str)
args = arg_parser.parse_args()

with open(args.config, 'r') as f:
    config = json.load(f)['data']
print(config)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', providers=config['providers'])

@app.route('/authenticate/<provider>')
def authenticate(provider):
    # Search for the provider in the config
    provider_config = next((p for p in config['providers'] if p['name'].lower() == provider), None)
    if provider_config is None:
        return jsonify({'error': 'Provider not found'}), 404
    client = WebApplicationClient(provider_config['clientId'])
    request_uri = client.prepare_request_uri(
        provider_config['endpoints']['authorize'],
        redirect_uri=f"{config['redirectUri']}/redirect/{provider}",
        scope='openid profile email'
    )
    print(request_uri)
    # Redirect the user to the authorization URL
    return redirect(request_uri)


@app.route('/redirect/<provider>')
def redirect_provider(provider):
    provider_config = next((p for p in config['providers'] if p['name'].lower() == provider), None)
    if provider_config is None:
        return jsonify({'error': 'Provider not found'}), 404
    client = WebApplicationClient(provider_config['clientId'])
    data = client.prepare_request_body(
        code = request.args.get('code'),
        redirect_uri=f"{config['redirectUri']}/redirect/{provider}",
        client_id=provider_config['clientId'],
        client_secret=provider_config['clientSecret']
    )
    accesstoken = requests.get(provider_config['endpoints']['accessToken'], data=data)
    client.parse_request_body_response(accesstoken.text)
    header = {'Authorization': f"Bearer {client.token['access_token']}"}
    userinfo = requests.get(provider_config['userinfo'], headers=header)
    print(userinfo.json())
    # Log the user in and redirect to the welcome page
    request.session['username'] = userinfo.json()['name']
    return render_template('welcome.html', userinfo=userinfo.json())


if __name__ == '__main__':
    app.run(port=args.port, debug=True)