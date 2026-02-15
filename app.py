from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # <-- QUESTO RISOLVE DEFINITIVAMENTE IL CORS

ruote = [
    "Bari","Cagliari","Firenze","Genova",
    "Milano","Napoli","Nazionale",
    "Palermo","Roma","Torino","Venezia"
]

def genera_dati():
    dati = {}
    for r in ruote:
        dati[r] = {
            "ultima_estrazione": random.sample(range(1, 91), 5),
            "previsione": random.sample(range(1, 91), 5)
        }
    return dati

@app.route("/")
def home():
    return "API Lotto attiva"

@app.route("/api")
def api():
    return jsonify(genera_dati())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)







