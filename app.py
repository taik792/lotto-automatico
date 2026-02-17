from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Server Lotto attivo 🚀"

@app.route("/api")
def api():
    try:
        with open("estrazioni.json", "r") as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"errore": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


























        











