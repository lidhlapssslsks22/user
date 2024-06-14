from flask import Flask, request, jsonify, render_template
import requests
import random
import string
from time import sleep

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('status.html')

@app.route('/check_username', methods=['POST'])
def check_username():
    data = request.get_json()
    username = data['username']

    headers = {'Authorization': 'OAuth oauth_consumer_key="BUHsuO5U9DF42uJtc8QTZlOmnUaJmBJGuU1efURxeklbdiLn9L", oauth_nonce="-6076367636842352338", oauth_signature="iqPuUk3HK3KA6DnwoLwO%2BqV%2BAME%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1716771084", oauth_token="q7LTQ2VAvwc53L7BjpeUUao9g7RSEun3P4usJsliPL17V9Sgax", oauth_version="1.0"'}
    response = requests.post(f'https://api-http2.tumblr.com/v2/blog/validate', data={'tumblelog': username}, headers=headers)

    if response.status_code == 200:
        return jsonify({'status': 'available', 'username': username})
    elif response.status_code == 400:
        return jsonify({'status': 'not_available', 'username': username})
    elif response.status_code == 429:
        sleep(0.9)
        return jsonify({'status': 'rate_limited'})
    else:
        return jsonify({'status': 'error', 'response': response.text})

@app.route('/start_batch_check', methods=['POST'])
def start_batch_check():
    results = []
    for _ in range(5): #Q_B_H
        username = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))
        headers = {'Authorization': 'OAuth oauth_consumer_key="BUHsuO5U9DF42uJtc8QTZlOmnUaJmBJGuU1efURxeklbdiLn9L", oauth_nonce="-6076367636842352338", oauth_signature="iqPuUk3HK3KA6DnwoLwO%2BqV%2BAME%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1716771084", oauth_token="q7LTQ2VAvwc53L7BjpeUUao9g7RSEun3P4usJsliPL17V9Sgax", oauth_version="1.0"'}
        response = requests.post(f'https://api-http2.tumblr.com/v2/blog/validate', data={'tumblelog': username}, headers=headers)

        if response.status_code == 200:
            results.append({'status': 'available', 'username': username})
        elif response.status_code == 400:
            results.append({'status': 'not_available', 'username': username})
        elif response.status_code == 429:
            sleep(0.9)
            results.append({'status': 'rate_limited'})
        else:
            results.append({'status': 'error', 'response': response.text})

    return jsonify({'results': results})

if __name__ == '__main__':
    app.run(debug=True)
