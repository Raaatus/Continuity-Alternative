from flask import Flask, request, jsonify

import json
from datetime import datetime
import os
script_dir = os.path.dirname(os.path.abspath(__file__))


app = Flask(__name__)

@app.route('/notification', methods=['POST'])
def notification_process():
    data = request.json
    print(data)
    return jsonify({"status": "success"}), 200

@app.route('/', methods=['GET'])
def checkonline():
    print(f"Test check serveur ONLINE")
    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)



