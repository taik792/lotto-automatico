from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from collections import Counter

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_ESTRAZIONI = os.path.join(BASE_DIR, "estrazioni.json")

FINESTRA_50 = 50
FINESTRA_100 = 100


def carica_dati():
    with open(FILE_ESTRAZIONI, "r", encoding="utf-8") as f:
        return json.load(f)


def analizza_ruota(lista_estrazioni):
    tutte = []
    for estrazione in lista_estrazioni:
        tutte.extend(estrazione)

    ultime_50 = tutte[-FINESTRA_50:]
    ultime_100 = tutte[-FINESTRA_100:]

    freq_totale = Counter(tutte)
    freq_50 = Counter(ultime_50)
    freq_100 = Counter(ultime_100)

    ritardi = {}
    for numero in range(1, 91):
        ritardo = 0
        for estrazione in reversed(lista_estrazioni):
            if numero in estrazione:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    pressione = {}
    for numero in range(1, 91):
        pressione[numero] = (
            freq_50[numero] * 3 +
            freq_100[numero] * 2 +
            freq_totale[numero]
        )

    caldi = [n for n, _ in freq_50.most_common(5)]
    freddi = sorted(ritardi, key=ritardi.get, reverse=True)[:5]
    ritardatario = max(ritardi, key=ritardi.get)
    suggeriti = sorted(pressione, key=pressione.get, reverse=True)[:3]

    indice_pressione = max(pressione.values())

    return {
        "ultima_estrazione": lista_estrazioni[-1] if lista_estrazioni else [],
        "caldi": caldi,
        "freddi": freddi,
        "ritardatario": ritardatario,
        "suggeriti": suggeriti,
        "indice_pressione": indice_pressione
    }


@app.route("/api")
def api():
    dati = carica_dati()
    risultato = {}

    for ruota, estrazioni in dati.items():
        risultato[ruota] = analizza_ruota(estrazioni)

    return jsonify(risultato)


@app.route("/")
def home():
    return "Backend Lotto attivo 🔥"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
