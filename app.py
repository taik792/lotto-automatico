from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

FILE_GIOCATE = "/tmp/giocate.json"
FILE_ESTRAZIONI = "estrazioni.json"

# -------------------------
# CARICA ESTRAZIONI
# -------------------------

def carica_estrazioni():
    if not os.path.exists(FILE_ESTRAZIONI):
        return {}

    with open(FILE_ESTRAZIONI, "r", encoding="utf-8") as f:
        return json.load(f)

# -------------------------
# API PRINCIPALE
# -------------------------

@app.route("/api", methods=["GET"])
def api():
    dati = carica_estrazioni()

    if not dati:
        return jsonify({"errore": "Nessun dato disponibile"})

    return jsonify(dati)

# -------------------------
# SALVA GIOCATA PREMIUM
# -------------------------

@app.route("/salva_giocata", methods=["POST"])
def salva_giocata():
    nuova = request.json

    if not os.path.exists(FILE_GIOCATE):
        with open(FILE_GIOCATE, "w") as f:
            json.dump([], f)

    with open(FILE_GIOCATE, "r") as f:
        giocate = json.load(f)

    nuova["data_attuale"] = datetime.now().strftime("%d/%m/%Y")
    giocate.append(nuova)

    with open(FILE_GIOCATE, "w") as f:
        json.dump(giocate, f)

    return jsonify({"messaggio": "Giocata salvata"})

# -------------------------
# MOSTRA GIOCATE ATTIVE
# -------------------------

@app.route("/giocate_attive", methods=["GET"])
def giocate_attive():
    if not os.path.exists(FILE_GIOCATE):
        return jsonify([])

    with open(FILE_GIOCATE, "r") as f:
        giocate = json.load(f)

    return jsonify(giocate)

# -------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
