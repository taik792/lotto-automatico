from flask import Flask, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

ruote = [
    "Bari", "Cagliari", "Firenze", "Genova",
    "Milano", "Napoli", "Palermo",
    "Roma", "Torino", "Venezia", "Nazionale"
]

def genera_estrazione():
    return random.sample(range(1, 91), 5)

def genera_ambo_prudente():
    return random.sample(range(1, 91), 2)

def genera_ambo_bilanciato():
    return random.sample(range(1, 91), 2)

def genera_ambo_ritardo():
    return random.sample(range(1, 91), 2)

@app.route("/api")
def api():
    dati = {}

    for ruota in ruote:
        dati[ruota] = {
            "ultima_estrazione": genera_estrazione(),
            "ambo_prudente": genera_ambo_prudente(),
            "ambo_bilanciato": genera_ambo_bilanciato(),
            "ambo_ritardo": genera_ambo_ritardo()
        }

    return jsonify(dati)

@app.route("/")
def home():
    return "API Lotto attiva"

if __name__ == "__main__":
    app.run()




        











