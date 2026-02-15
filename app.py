from flask import Flask, jsonify
from flask_cors import CORS
import json
import random

app = Flask(__name__)
CORS(app)

# Ruote ufficiali
RUOTE = [
    "Bari", "Cagliari", "Firenze", "Genova",
    "Milano", "Napoli", "Palermo", "Roma",
    "Torino", "Venezia", "Nazionale"
]

# Carica estrazioni dal file locale
def carica_dati():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

# Genera ambo prudente (numeri bassi frequenti)
def genera_ambo_prudente(estrazione):
    numeri = sorted(estrazione)
    return numeri[:2]

# Genera ambo bilanciato (uno basso uno alto)
def genera_ambo_bilanciato(estrazione):
    numeri = sorted(estrazione)
    return [numeri[0], numeri[-1]]

# Genera ambo ritardo (simulazione casuale)
def genera_ambo_ritardo():
    return random.sample(range(1, 91), 2)

# Genera terno strategico
def genera_terno(estrazione):
    numeri = sorted(estrazione)
    return numeri[:3]

# Analizza singola ruota
def analizza_ruota(estrazioni_ruota):
    ultima = estrazioni_ruota[0]

    return {
        "ultima_estrazione": ultima,
        "ambo_prudente": genera_ambo_prudente(ultima),
        "ambo_bilanciato": genera_ambo_bilanciato(ultima),
        "ambo_ritardo": genera_ambo_ritardo(),
        "terno_strategico": genera_terno(ultima)
    }

@app.route("/api")
def api():
    try:
        dati = carica_dati()
        risultato = {}

        for ruota in RUOTE:
            if ruota in dati:
                risultato[ruota] = analizza_ruota(dati[ruota])

        return jsonify(risultato)

    except Exception as e:
        return jsonify({"errore": str(e)})

@app.route("/")
def home():
    return "API Lotto attiva"








        











