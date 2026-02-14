from flask import Flask, jsonify
import random

app = Flask(__name__)

ruote = [
    "Bari", "Cagliari", "Firenze", "Genova",
    "Milano", "Napoli", "Nazionale",
    "Palermo", "Roma", "Torino", "Venezia"
]

def genera_numeri():
    return sorted(random.sample(range(1, 91), 5))

@app.route("/api")
def api():
    dati = {}

    for ruota in ruote:
        dati[ruota] = {
            "ultima_estrazione": genera_numeri(),
            "previsione": genera_numeri()
        }

    return jsonify(dati)

@app.route("/")
def home():
    return "API Lotto attiva"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)





