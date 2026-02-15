from flask import Flask, jsonify
from flask_cors import CORS
import os
import requests
import base64

app = Flask(__name__)
CORS(app)  # <-- QUESTA È LA PARTE IMPORTANTE

TOKEN = os.getenv("TOKEN")

def carica_estrazioni():
    url = "https://api.github.com/repos/taik792/lotto-automatico/contents/estrazioni.json"
    headers = {
        "Authorization": f"token {TOKEN}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    contenuto = base64.b64decode(data["content"]).decode("utf-8")

    import json
    return json.loads(contenuto)

@app.route("/")
def home():
    return "API Lotto attiva"

@app.route("/api")
def api():
    try:
        dati = carica_estrazioni()
        return jsonify(dati)
    except Exception as e:
        return jsonify({"errore": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)























        











