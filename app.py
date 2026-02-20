from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

FILE_GIOCATE = "/tmp/giocate.json"

# =========================
# CREA FILE SE NON ESISTE
# =========================
if not os.path.exists(FILE_GIOCATE):
    with open(FILE_GIOCATE, "w") as f:
        json.dump([], f)

# =========================
# ROUTE TEST
# =========================
@app.route("/")
def home():
    return "Backend Lotto Attivo"

# =========================
# SALVA GIOCATA
# =========================
@app.route("/salva_giocata", methods=["POST"])
def salva_giocata():
    data = request.json

    if not data:
        return jsonify({"errore": "Nessun dato ricevuto"}), 400

    with open(FILE_GIOCATE, "r") as f:
        giocate = json.load(f)

    giocate.append(data)

    with open(FILE_GIOCATE, "w") as f:
        json.dump(giocate, f)

    return jsonify({"status": "ok", "giocate_totali": len(giocate)})

# =========================
# RESTITUISCE GIOCATE ATTIVE
# =========================
@app.route("/giocate_attive", methods=["GET"])
def giocate_attive():
    with open(FILE_GIOCATE, "r") as f:
        giocate = json.load(f)

    return jsonify(giocate)

# =========================
# RESET GIOCATE
# =========================
@app.route("/reset_giocate", methods=["POST"])
def reset_giocate():
    with open(FILE_GIOCATE, "w") as f:
        json.dump([], f)

    return jsonify({"status": "reset completato"})

# =========================
# AVVIO APP
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
