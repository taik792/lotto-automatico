from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# ===== CARICAMENTO DATI SICURO =====
try:
    with open("estrazioni.json", "r") as f:
        raw_data = json.load(f)
except Exception as e:
    print("Errore caricamento JSON:", e)
    raw_data = {}

# Se i dati sono dentro "ruote", li prendiamo
if isinstance(raw_data, dict) and "ruote" in raw_data:
    dati = raw_data["ruote"]
else:
    dati = raw_data


@app.route("/")
def home():
    return "Lotto Live Statistiche API attiva"


@app.route("/api")
def api():

    mode = request.args.get("mode", "prudente")

    risultati = []
    ruota_piu_forte = None
    punteggio_massimo = -1

    for ruota, estrazioni in dati.items():

        # Se non è lista, salta
        if not isinstance(estrazioni, list):
            continue

        if len(estrazioni) == 0:
            continue

        # Garantiamo che ogni estrazione sia lista di numeri
        estrazioni_pulite = [
            e for e in estrazioni if isinstance(e, list)
        ]

        if len(estrazioni_pulite) == 0:
            continue

        ultime_20 = estrazioni_pulite[-20:]
        ultime_5 = estrazioni_pulite[-5:]
        ultima = estrazioni_pulite[-1]

        freq_totale = sum(len(e) for e in ultime_20)
        trend = sum(len(e) for e in ultime_5)
        penalita = len(ultima)

        # ===== ALGORITMO INTELLIGENTE =====
        if mode == "prudente":
            score = (freq_totale * 2) + (trend * 1) - (penalita * 1)
        else:
            score = (freq_totale * 1) + (trend * 3) - (penalita * 0.5)

        risultati.append({
            "ruota": ruota,
            "numeri": ultima,
            "score": round(score, 2)
        })

        if score > punteggio_massimo:
            punteggio_massimo = score
            ruota_piu_forte = ruota

    return jsonify({
        "modalita": mode,
        "ruota_piu_forte": ruota_piu_forte,
        "ruote": risultati
    })


# ===== AVVIO CORRETTO PER RENDER =====
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)



















        











