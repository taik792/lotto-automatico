from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# ===============================
# CARICA ESTRIZIONI UNA SOLA VOLTA
# ===============================

with open("estrazioni.json") as f:
    ESTRAZIONI = json.load(f)

# ===============================
# API LEGGERA (solo ultime 5)
# ===============================

@app.route("/api")
def api():
    risposta = {}

    for ruota, estrazioni in ESTRAZIONI.items():
        risposta[ruota] = estrazioni[:5]  # solo ultime 5

    return jsonify(risposta)

# ===============================
# SALVA GIOCATA PREMIUM
# ===============================

FILE_GIOCATE = "/tmp/giocate.json"

def carica_giocate():
    if not os.path.exists(FILE_GIOCATE):
        return []
    with open(FILE_GIOCATE, "r") as f:
        return json.load(f)

def salva_giocate(lista):
    with open(FILE_GIOCATE, "w") as f:
        json.dump(lista, f)

@app.route("/salva_giocata", methods=["POST"])
def salva_giocata():
    dati = request.get_json()

    num1 = dati.get("num1")
    num2 = dati.get("num2")
    ruota = dati.get("ruota")

    giocate = carica_giocate()

    nuova = {
        "num1": num1,
        "num2": num2,
        "ruota": ruota,
        "stato": "attivo"
    }

    giocate.append(nuova)
    salva_giocate(giocate)

    return jsonify({"status": "ok"})

# ===============================
# LISTA GIOCATE ATTIVE
# ===============================

@app.route("/giocate_attive")
def giocate_attive():
    giocate = carica_giocate()
    return jsonify(giocate)

# ===============================
# AVVIO SERVER RENDER
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
