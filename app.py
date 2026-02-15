from flask import Flask, jsonify
from flask_cors import CORS
import random
from collections import Counter

app = Flask(__name__)
CORS(app)

RUOTE = [
    "Bari", "Cagliari", "Firenze", "Genova",
    "Milano", "Napoli", "Palermo", "Roma",
    "Torino", "Venezia", "Nazionale"
]

def genera_estrazione():
    return sorted(random.sample(range(1, 91), 5))

def genera_previsione(storico):
    tutti_numeri = [n for estr in storico for n in estr]
    frequenze = Counter(tutti_numeri)

    freddi = sorted(frequenze, key=frequenze.get)[:10]
    if len(freddi) >= 5:
        return sorted(random.sample(freddi, 5))
    else:
        return sorted(random.sample(range(1, 91), 5))

@app.route("/")
def home():
    return "API Lotto attiva"

@app.route("/api")
def api():
    dati = {}

    for ruota in RUOTE:
        storico = [genera_estrazione() for _ in range(20)]
        ultima = storico[-1]
        previsione = genera_previsione(storico)

        dati[ruota] = {
            "ultima_estrazione": ultima,
            "previsione": previsione
        }

    return jsonify(dati)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

        











