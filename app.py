from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # 🔥 Permette richieste da GitHub Pages

GIOCATE_FILE = "/tmp/giocate.json"

# -------------------------
# CREAZIONE FILE SE NON ESISTE
# -------------------------
def init_giocate():
    if not os.path.exists(GIOCATE_FILE):
        with open(GIOCATE_FILE, "w") as f:
            json.dump([], f)

def carica_giocate():
    init_giocate()
    with open(GIOCATE_FILE, "r") as f:
        return json.load(f)

def salva_giocate(data):
    with open(GIOCATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -------------------------
# SALVA PREMIUM
# -------------------------
@app.route("/salva-premium", methods=["POST"])
def salva_premium():
    data = request.json

    nuova = {
        "tipo": data["tipo"],
        "numeri": data["numeri"],
        "ruota": data["ruota"],
        "durata": int(data["durata"]),
        "estrazioni_passate": 0,
        "stato": "ATTIVO",
        "data_creazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    giocate = carica_giocate()
    giocate.append(nuova)
    salva_giocate(giocate)

    return jsonify({"ok": True})

# -------------------------
# TEST SALVATAGGIO VIA BROWSER
# -------------------------
@app.route("/test-salva")
def test_salva():
    nuova = {
        "tipo": "ambo",
        "numeri": [21, 48],
        "ruota": "Venezia",
        "durata": 5,
        "estrazioni_passate": 0,
        "stato": "ATTIVO",
        "data_creazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    giocate = carica_giocate()
    giocate.append(nuova)
    salva_giocate(giocate)

    return "Giocata salvata!"

# -------------------------
# MOSTRA GIOCATE ATTIVE
# -------------------------
@app.route("/giocate-attive")
def giocate_attive():
    giocate = carica_giocate()
    attive = [g for g in giocate if g["stato"] == "ATTIVO"]
    return jsonify(attive)

# -------------------------
# AGGIORNA DOPO NUOVA ESTRAZIONE
# -------------------------
@app.route("/aggiorna-estrazione", methods=["POST"])
def aggiorna_estrazione():
    estrazione = request.json  # {"ruota": "Venezia", "numeri": [10,20,30,40,50]}

    giocate = carica_giocate()

    for g in giocate:
        if g["stato"] == "ATTIVO" and g["ruota"] == estrazione["ruota"]:

            # Controllo vincita
            if all(num in estrazione["numeri"] for num in g["numeri"]):
                g["stato"] = "VINCENTE"
            else:
                g["estrazioni_passate"] += 1
                if g["estrazioni_passate"] >= g["durata"]:
                    g["stato"] = "SCADUTA"

    salva_giocate(giocate)
    return jsonify({"ok": True})

# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    return "Backend Lotto Premium Attivo"

# -------------------------
# AVVIO
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
