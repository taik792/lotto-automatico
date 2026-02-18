from flask import Flask, jsonify
from flask_cors import CORS
import json
from collections import Counter
import random

app = Flask(__name__)
CORS(app)

def calcola_statistiche(dati_ruota):

    if not dati_ruota or len(dati_ruota) == 0:
        return [], [], 0, 0, []

    # Limitiamo agli ultimi 400 concorsi per performance
    dati_ruota = dati_ruota[-400:]

    tutte_estrazioni = []
    for estrazione in dati_ruota:
        tutte_estrazioni.extend(estrazione)

    conteggio = Counter(tutte_estrazioni)

    numeri_caldi = [num for num, _ in conteggio.most_common(5)]

    tutti_numeri = set(range(1, 91))
    numeri_presenti = set(tutte_estrazioni)
    numeri_assenti = list(tutti_numeri - numeri_presenti)

    numeri_freddi = numeri_assenti if len(numeri_assenti) >= 5 else list(tutti_numeri)

    ritardi = {}
    for numero in tutti_numeri:
        ritardo = 0
        for estrazione in reversed(dati_ruota):
            if numero in estrazione:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    ritardo_massimo = max(ritardi.values()) if ritardi else 0

    indice_pressione = round(
        (ritardo_massimo * 0.6) +
        (sum(sorted(ritardi.values(), reverse=True)[:5]) * 0.4 / 5),
        2
    )

    combinazioni = []

    for _ in range(3):
        combo = []

        caldi_pool = numeri_caldi if len(numeri_caldi) >= 2 else list(tutti_numeri)
        freddi_pool = numeri_freddi if len(numeri_freddi) >= 2 else list(tutti_numeri)

        combo += random.sample(caldi_pool, 2)
        combo += random.sample(freddi_pool, 2)

        restante = list(tutti_numeri - set(combo))
        if len(restante) >= 1:
            combo += random.sample(restante, 1)

        combinazioni.append(sorted(combo))

    return (
        numeri_caldi[:3],
        numeri_freddi[:3],
        ritardo_massimo,
        indice_pressione,
        combinazioni
    )


@app.route("/api")
def api():
    try:
        with open("estrazioni.json", "r") as file:
            dati = json.load(file)

        risultato = {}
        pressione_massima = -1
        ruota_forte = None

        for ruota, estrazioni in dati.items():

            caldi, freddi, ritardo, pressione, combinazioni = calcola_statistiche(estrazioni)

            risultato[ruota] = {
                "ultima_estrazione": estrazioni[-1] if estrazioni else [],
                "numeri_caldi": caldi,
                "numeri_freddi": freddi,
                "ritardo_massimo": ritardo,
                "indice_pressione": pressione,
                "combinazioni_suggerite": combinazioni
            }

            if pressione > pressione_massima:
                pressione_massima = pressione
                ruota_forte = ruota

        risultato["ruota_piu_forte"] = ruota_forte

        return jsonify(risultato)

    except Exception as e:
        return jsonify({"errore": str(e)})


if __name__ == "__main__":
    app.run()
























        











