from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
import base64

app = Flask(__name__)
CORS(app)  # <-- QUESTA RIGA È FONDAMENTALE

TOKEN = os.environ.get("TOKEN")

GITHUB_URL = "https://api.github.com/repos/taik792/lotto-automatico/contents/estrazioni.json"

@app.route("/api")
def get_data():
    headers = {
        "Authorization": f"token {TOKEN}"
    }

    response = requests.get(GITHUB_URL, headers=headers)

    if response.status_code != 200:
        return jsonify({"errore": "Errore GitHub"}), 500

    content = response.json()["content"]
    decoded = base64.b64decode(content).decode("utf-8")

    import json
    data = json.loads(decoded)

    return jsonify(data)

@app.route("/")
def home():
    return "API attiva"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)





















        











