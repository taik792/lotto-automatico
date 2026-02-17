from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# ===== CARICA DATI ESTRAZIONI =====
with open("estrazioni.json", "r") as f:
    dati = json.load(f)

@app.route("/api")
def api():

    mode = request.args.get("mode", "prudente")

    risultati = []
    ruota_piu_forte = None
    punteggio_massimo = -1

    for ruota, estrazioni in dati.items():

        # Assicuriamoci che siano liste valide
        if len(estrazioni) < 5:
            continue

        ultime_20 = estrazioni[-20:] if len(estrazioni) >= 20 else estrazioni
        ultime_5 = estrazioni[-5:]
        ultima = estrazioni[-1]

        freq_totale = 0
        trend = 0
        penalita = 0

        # Frequenza totale ultimi 20
        for estrazione in ultime_20:
            freq_totale += len(estrazione)

        # Trend ultime 5
        for estrazione in ultime_5:
            trend += len(estrazione)

        # Penalità numeri appena usciti
        penalita = len(ultima)

        # ===== CALCOLO PUNTEGGIO INTELLIGENTE =====
        if mode == "prudente":
            score = (freq_totale * 2) + (trend * 1) - (penalita * 1)
        else:  # aggressiva
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


if __name__ == "__main__":
    app.run(debug=True)





















        











