from flask import Flask, request, jsonify, send_from_directory
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='.', static_url_path='')

SIGNUPS_FILE = 'signups.json'


def load_signups():
    try:
        with open(SIGNUPS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []


def save_signups(signups):
    with open(SIGNUPS_FILE, 'w') as f:
        json.dump(signups, f)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not data.get('email'):
        return jsonify({'error': 'No email'}), 400

    email = data['email'].strip().lower()
    signups = load_signups()

    for s in signups:
        if s['email'] == email:
            return jsonify({'message': 'Already signed up', 'count': len(signups)})

    signups.append({
        'email': email,
        'signed_up_at': datetime.utcnow().isoformat(),
    })
    save_signups(signups)

    print('[AWE] New signup: ' + email + ' | Total: ' + str(len(signups)))

    return jsonify({'message': 'Welcome', 'count': len(signups)})


@app.route('/api/count')
def count():
    signups = load_signups()
    return jsonify({'count': len(signups)})


@app.route('/api/signups')
def list_signups():
    signups = load_signups()
    return jsonify({'count': len(signups), 'signups': signups})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
