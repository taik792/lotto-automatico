from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from collections import Counter

app = Flask(__name__)
CORS(app)

# ===== CARICAMENTO DATI =====
try:
    with open("estrazioni.json", "r") as f:
        raw_data = json.load(f)
except:
    raw_data = {}

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
    punteggi = []

    for ruota, estrazioni in dati.items():

        if not isinstance(estrazioni, list) or len(estrazioni) == 0:
            continue

        estrazioni = [e for e in estrazioni if isinstance(e, list)]
        if len(estrazioni) == 0:
            continue

        ultime_20 = estrazioni[-20:]
        ultime_5 = estrazioni[-5:]
        ultima = estrazioni[-1]

        numeri_20 = [n for e in ultime_20 for n in e]
        numeri_5 = [n for e in ultime_5 for n in e]

        freq_20 = Counter(numeri_20)
        freq_5 = Counter(numeri_5)

        score = 0

        for numero in ultima:

            f20 = freq_20.get(numero, 0)
            f5 = freq_5.get(numero, 0)

            if mode == "prudente":
                score += (f20 * 3) + (f5 * 1)
            else:
                score += (f5 * 4) + (f20 * 1)

        punteggi.append(score)

        risultati.append({
            "ruota": ruota,
            "numeri": ultima,
            "score": score
        })

    if not risultati:
        return jsonify({
            "modalita": mode,
            "ruota_piu_forte": None,
            "ruote": []
        })

    max_score = max(punteggi)
    min_score = min(punteggi)

    for r in risultati:
        if max_score == min_score:
            percentuale = 50
        else:
            percentuale = ((r["score"] - min_score) / (max_score - min_score)) * 100

        r["percentuale"] = round(percentuale, 1)

    ruota_piu_forte = max(risultati, key=lambda x: x["percentuale"])["ruota"]

    return jsonify({
        "modalita": mode,
        "ruota_piu_forte": ruota_piu_forte,
        "ruote": risultati
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)





















        











