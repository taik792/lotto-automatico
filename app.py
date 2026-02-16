from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

# Carica dati dal file estrazioni.json
def carica_dati():
    with open("estrazioni.json", "r") as file:
        return json.load(file)

@app.route("/")
def home():
    return "Server Lotto attivo 🚀"

@app.route("/api")
def api():
    try:
        dati = carica_dati()
        return jsonify(dati)
    except Exception as e:
        return jsonify({"errore": str(e)}), 500


# 🔥 PARTE FONDAMENTALE PER RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

























        











