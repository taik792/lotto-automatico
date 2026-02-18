from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from collections import Counter

app = Flask(__name__)
CORS(app)


# ===============================
# CARICAMENTO DATI
# ===============================

def carica_dati():
    with open("estrazioni.json", "r") as f:
        return json.load(f)


# ===============================
# CALCOLO STATISTICHE
# ===============================

def calcola_statistiche(nome_ruota, estrazioni):

    tutte_estrazioni = estrazioni
    ultima_estrazione = estrazioni[-1]

    # -------------------------
    # NUMERI CALDI (frequenza totale)
    # -------------------------
    contatore = Counter()

    for estrazione in tutte_estrazioni:
        for numero in estrazione:
            contatore[numero] += 1

    numeri_caldi = [n for n, _ in contatore.most_common(3)]

    # -------------------------
    # NUMERI FREDDI (meno frequenti)
    # -------------------------
    numeri_freddi = sorted(contatore.items(), key=lambda x: x[1])[:3]
    numeri_freddi = [n[0] for n in numeri_freddi]

    # -------------------------
    # RITARDI
    # -------------------------
    ritardi = {}
    totale_estrazioni = len(tutte_estrazioni)

    for numero in range(1, 91):
        ritardo = 0
        trovato = False

        for i in range(totale_estrazioni - 1, -1, -1):
            if numero in tutte_estrazioni[i]:
                trovato = True
                break
            ritardo += 1

        if not trovato:
            ritardo = totale_estrazioni

        ritardi[numero] = ritardo

    ritardo_massimo = max(ritardi.values())

    # -------------------------
    # INDICE PRESSIONE (NUOVO STEP AVANZATO)
    # -------------------------
    media_ritardi = sum(ritardi.values()) / 90
    indice_pressione = round((ritardo_massimo * 0.6) + (media_ritardi * 0.4), 2)

    # -------------------------
    # COMBINAZIONI SUGGERITE
    # -------------------------
    combinazioni = []
    for i in range(3):
        combo = []
        combo.append(numeri_caldi[i % len(numeri_caldi)])
        combo.append(numeri_freddi[i % len(numeri_freddi)])
        combo.append(sorted(ritardi, key=ritardi.get, reverse=True)[i])
        combo.append(ultima_estrazione[i])
        combo.append(ultima_estrazione[-(i+1)])
        combinazioni.append(combo)

    return {
        "ruota": nome_ruota,
        "ultima_estrazione": ultima_estrazione,
        "numeri_caldi": numeri_caldi,
        "numeri_freddi": numeri_freddi,
        "ritardo_massimo": ritardo_massimo,
        "indice_pressione": indice_pressione,
        "combinazioni_suggerite": combinazioni
    }


# ===============================
# API
# ===============================

@app.route("/api")
def api():

    dati = carica_dati()
    risultato = []

    for ruota, estrazioni in dati.items():
        stats = calcola_statistiche(ruota, estrazioni)
        risultato.append(stats)

    ruota_forte = max(risultato, key=lambda x: x["indice_pressione"])

    return jsonify({
        "ruota_piu_forte": ruota_forte["ruota"],
        "dettagli": risultato
    })


# ===============================
# AVVIO PER RENDER
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
























        











