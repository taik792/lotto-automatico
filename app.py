from flask import Flask, jsonify
from flask_cors import CORS
import json
from collections import Counter
import os

app = Flask(__name__)
CORS(app)

FILE_ESTRAZIONI = "estrazioni.json"

FINESTRA_50 = 50
FINESTRA_100 = 100

def carica_dati():
    with open(FILE_ESTRAZIONI, "r", encoding="utf-8") as f:
        return json.load(f)

def analizza_ruota(estrazioni, ruota):
    tutte = []
    
    for estrazione in estrazioni:
        if ruota in estrazione:
            tutte.extend(estrazione[ruota])

    totale = len(tutte)

    ultimi_50 = tutte[-FINESTRA_50:]
    ultimi_100 = tutte[-FINESTRA_100:]

    freq_totale = Counter(tutte)
    freq_50 = Counter(ultimi_50)
    freq_100 = Counter(ultimi_100)

    # Numeri caldi (top 5 ultimi 50)
    caldi = [n for n, _ in freq_50.most_common(5)]

    # Numeri freddi (mai usciti ultimi 100)
    freddi = [n for n in range(1, 91) if freq_100[n] == 0][:5]

    # Ritardatario
    ritardi = {}
    for numero in range(1, 91):
        ritardo = 0
        for n in reversed(tutte):
            if n != numero:
                ritardo += 1
            else:
                break
        ritardi[numero] = ritardo

    ritardatario = max(ritardi, key=ritardi.get)

    # Indice pressione
    pressione = {}
    for numero in range(1, 91):
        pressione[numero] = (
            freq_50[numero] * 3 +
            freq_100[numero] * 2 +
            freq_totale[numero]
        )

    pressione_ordinata = sorted(pressione.items(), key=lambda x: x[1], reverse=True)
    suggeriti = [n for n, _ in pressione_ordinata[:5]]

    return {
        "caldi": caldi,
        "freddi": freddi,
        "ritardatario": ritardatario,
        "suggeriti": suggeriti,
        "pressione_top": suggeriti
    }

@app.route("/api")
def api():
    try:
        estrazioni = carica_dati()
        risultato = {}
        punteggi_ruote = {}

        for ruota in estrazioni[0].keys():
            analisi = analizza_ruota(estrazioni, ruota)
            risultato[ruota] = analisi
            punteggi_ruote[ruota] = sum(analisi["pressione_top"])

        ruota_forte = max(punteggi_ruote, key=punteggi_ruote.get)

        return jsonify({
            "ruota_forte": ruota_forte,
            "dati": risultato
        })

    except Exception as e:
        return jsonify({"errore": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

























        











