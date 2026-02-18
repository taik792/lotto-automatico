from flask import Flask, jsonify
from flask_cors import CORS
import json
import random
from collections import Counter

app = Flask(__name__)
CORS(app)

def carica_dati():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

def calcola_statistiche(ruota, estrazioni):

    totale_estrazioni = len(estrazioni)
    ultima = estrazioni[-1]

    # ---- Frequenza totale ----
    tutti_numeri = [num for estr in estrazioni for num in estr]
    frequenze = Counter(tutti_numeri)

    # ---- Numeri caldi ----
    numeri_caldi = [n for n, _ in frequenze.most_common(3)]

    # ---- Ritardi ----
    ritardi = {}
    for numero in range(1, 91):
        ritardo = 0
        for estr in reversed(estrazioni):
            if numero in estr:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    ritardo_massimo = max(ritardi.values())
    ritardo_medio = sum(ritardi.values()) / 90

    # ---- Frequenza ultimi 20 concorsi ----
    ultimi_20 = estrazioni[-20:] if totale_estrazioni >= 20 else estrazioni
    numeri_recenti = [n for estr in ultimi_20 for n in estr]
    freq_recenti = Counter(numeri_recenti)

    pressione_recenti = sum(freq_recenti.values())

    # ---- INDICE PRESSIONE ----
    indice_pressione = (
        ritardo_medio * 0.4 +
        ritardo_massimo * 0.4 +
        pressione_recenti * 0.2
    )

    # ---- Combinazioni suggerite ----
    combinazioni = []
    numeri_forti = sorted(ritardi, key=ritardi.get, reverse=True)[:15]

    for _ in range(3):
        combinazioni.append(sorted(random.sample(numeri_forti, 5)))

    return {
        "ruota": ruota,
        "ultima_estrazione": ultima,
        "numeri_caldi": numeri_caldi,
        "ritardo_massimo": ritardo_massimo,
        "ritardo_medio": round(ritardo_medio, 2),
        "indice_pressione": round(indice_pressione, 2),
        "combinazioni_suggerite": combinazioni
    }

@app.route("/api")
def api():

    dati = carica_dati()
    risultato = []

    for ruota, estrazioni in dati.items():
        stats = calcola_statistiche(ruota, estrazioni)
        risultato.append(stats)

    # ---- Trova ruota più in pressione ----
    ruota_forte = max(risultato, key=lambda x: x["indice_pressione"])

    return jsonify({
        "ruota_piu_forte": ruota_forte["ruota"],
        "dettagli": risultato
    })

if __name__ == "__main__":
    app.run(debug=True)























        











