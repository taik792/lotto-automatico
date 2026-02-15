from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
import base64

app = Flask(__name__)
CORS(app)

GITHUB_TOKEN = os.environ.get("TOKEN")

REPO_OWNER = "taik792"
REPO_NAME = "lotto-automatico"
FILE_PATH = "estrazioni.json"

@app.route("/")
def home():
    return "API Lotto attiva"

@app.route("/api")
def get_data():
    try:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_PATH}"
        
        headers = {
            "Authorization": f"token {GITHUB_TOKEN}"
        }

        response = requests.get(url, headers=headers)
        data = response.json()

        if "content" not in data:
            return jsonify({"errore": data})

        content = base64.b64decode(data["content"]).decode("utf-8")
        return content

    except Exception as e:
        return jsonify({"errore": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


















        











