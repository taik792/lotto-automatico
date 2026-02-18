from flask import Flask, jsonify
from flask_cors import CORS
import json
from collections import Counter
import os
import random

app = Flask(__name__)
CORS(app)

def calcola_statistiche(dati_ruota):

    tutte_estrazioni = []
    for estrazione in dati_ruota:
        tutte_estrazioni.extend(estrazione)

    conteggio = Counter(tutte_estrazioni)

    numeri_caldi = [num for num, _ in conteggio.most_common(5)]

    tutti_numeri = set(range(1, 91))
    numeri_presenti = set(tutte_estrazioni)
    numeri_assenti = list(tutti_numeri - numeri_presenti)

    numeri_freddi = numeri_assenti[:5]

    ritardi = {}
    for numero in tutti_numeri:
        ritardo = 0
        for estrazione in reversed(dati_ruota):
            if numero in estrazione:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    ritardo_massimo = max(ritardi.values())

    indice_pressione = round(
        (ritardo_massimo * 0.6) +
        (sum([ritardi[n] for n in numeri_freddi[:3]]) * 0.4),
        2
    )

    # 🔥 COMBINAZIONI PIÙ VARIE
    combinazioni = []
    for _ in range(3):
        combo = []
        combo += random.sample(numeri_caldi, 2)
        combo += random.sample(numeri_freddi[:10], 2)
        combo += random.sample(list(tutti_numeri), 1)
        combinazioni.append(sorted(combo))

    return numeri_caldi[:3], numeri_freddi[:3], ritardo_massimo, indice_pressione, combinazioni


@app.route("/api")
def api():

    try:
        with open("estrazioni.json", "r") as file:
            dati = json.load(file)

        risultato = []
        ruota_piu_forte = None
        pressione_massima = 0

        for ruota, estrazioni in dati.items():

            numeri_caldi, numeri_freddi, ritardo_massimo, indice_pressione, combinazioni = calcola_statistiche(estrazioni)

            if indice_pressione > pressione_massima:
                pressione_massima = indice_pressione
                ruota_piu_forte = ruota

            risultato.append({
                "ruota": ruota,
                "ultima_estrazione": estrazioni[-1] if len(estrazioni) > 0 else [],
                "numeri_caldi": numeri_caldi,
                "numeri_freddi": numeri_freddi,
                "ritardo_massimo": ritardo_massimo,
                "indice_pressione": indice_pressione,
                "combinazioni_suggerite": combinazioni
            })

        return jsonify({
            "ruote": risultato,
            "ruota_piu_forte": ruota_piu_forte
        })

    except Exception as e:
        return jsonify({"errore": str(e)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

























        











