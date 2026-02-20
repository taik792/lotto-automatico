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

    freq_totale = Counter(tutte)

    ultimi_50 = tutte[-FINESTRA_50:]
    ultimi_100 = tutte[-FINESTRA_100:]

    freq_50 = Counter(ultimi_50)
    freq_100 = Counter(ultimi_100)

    # Caldi
    caldi = [n for n, _ in freq_50.most_common(5)]

    # Freddi
    freddi = [n for n, _ in freq_50.most_common()[:-6:-1]]

    # Ritardatario
    ritardi = {}
    for numero in range(1, 91):
        ritardo = 0
        for estrazione in reversed(lista_estrazioni):
            if numero in estrazione:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    ritardatario = max(ritardi, key=ritardi.get)

    # 3 numeri da giocare
    suggeriti = list(set(caldi[:2] + [ritardatario]))[:3]

    # Sistema Ambi forti (caldo + ritardatario)
    ambi = []
    for caldo in caldi[:3]:
        ambi.append((caldo, ritardatario))

    # Indice pressione
    indice_pressione = sum(freq_50.values()) + sum(freq_100.values()) + ritardi[ritardatario]

    ultima_estrazione = lista_estrazioni[-1] if lista_estrazioni else []

    return {
        "caldi": caldi,
        "freddi": freddi,
        "ritardatario": ritardatario,
        "da_giocare": suggeriti,
        "ambi_forti": ambi,
        "indice_pressione": indice_pressione,
        "ultima_estrazione": ultima_estrazione
    }

@app.route("/api")
def api():

    dati = carica_dati()
    risultato = {}

    pressione_massima = 0
    ruota_forte = ""

    for ruota, estrazioni in dati.items():

        stats = analizza_ruota(estrazioni)

        risultato[ruota] = stats

        if stats["indice_pressione"] > pressione_massima:
            pressione_massima = stats["indice_pressione"]
            ruota_forte = ruota

    # Segna ruota forte
    risultato["ruota_forte"] = ruota_forte

    return jsonify(risultato)

@app.route("/")
def home():
    return "Backend Lotto Statistiche attivo"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
