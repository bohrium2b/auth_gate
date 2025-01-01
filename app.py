from flask import Flask, request, jsonify, render_template, redirect
import json
from oauthlib.oauth2 import WebApplicationClient
from argparse import ArgumentParser

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
    authorization_url = client.prepare_authorization_request(
        provider_config['endpoints']['authorize'],
        redirect_uri=f"{config['redirectUri']}/redirect/{provider}",
        scope='openid profile email'
    )
    # Redirect the user to the authorization URL
    return redirect(authorization_url)


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
    accesstoken = requests.get(provider_config['access_token'], data=data)
    client.parse_request_body_response(accesstoken.text)
    header = {'Authorization': f"Bearer {client.token['access_token']}"}
    userinfo = requests.get(provider_config['userinfo'], headers=header)
    print(userinfo.json())
    return render_template('welcome.html', userinfo=userinfo.json())


if __name__ == '__main__':
    app.run(port=args.port, debug=True)