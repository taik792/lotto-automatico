from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from collections import Counter
import random

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

    risultati = []

    for ruota, estrazioni in dati.items():

        if not isinstance(estrazioni, list) or len(estrazioni) == 0:
            continue

        estrazioni = [e for e in estrazioni if isinstance(e, list)]
        ultima = estrazioni[-1]

        # ===== NUMERI ULTIME 10 =====
        ultime_10 = estrazioni[-10:]
        numeri_10 = [n for e in ultime_10 for n in e]
        freq_10 = Counter(numeri_10)

        # 🔥 Numeri caldi (top 3)
        numeri_caldi = [n for n, _ in freq_10.most_common(3)]

        # ===== RITARDI =====
        tutti_numeri = list(range(1, 91))
        ritardi = {}

        for numero in tutti_numeri:
            ritardo = 0
            for estr in reversed(estrazioni):
                if numero in estr:
                    break
                ritardo += 1
            ritardi[numero] = ritardo

        # ❄️ Numeri freddi (top 3 ritardo massimo)
        numeri_freddi = sorted(ritardi, key=ritardi.get, reverse=True)[:3]

        # ⏳ Ritardo massimo della ruota
        ritardo_massimo = max(ritardi.values())

        # 🎲 Simulatore combinazioni (3 combinazioni casuali)
        combinazioni = []
        for _ in range(3):
            combinazione = sorted(random.sample(range(1, 91), 5))
            combinazioni.append(combinazione)

        risultati.append({
            "ruota": ruota,
            "ultima_estrazione": ultima,
            "numeri_caldi": numeri_caldi,
            "numeri_freddi": numeri_freddi,
            "ritardo_massimo": ritardo_massimo,
            "combinazioni_suggerite": combinazioni
        })

    return jsonify({
        "ruote": risultati
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)






















        











