from flask import Flask, jsonify
from flask_cors import CORS
import json
import random
from collections import Counter

app = Flask(__name__)
CORS(app)

# ================================
# CARICAMENTO DATI
# ================================
def carica_dati():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

# ================================
# CALCOLO FREQUENZE PESATE 50/100
# ================================
def calcola_punteggi(estrazioni):
    ultime_50 = estrazioni[-50:] if len(estrazioni) >= 50 else estrazioni
    ultime_100 = estrazioni[-100:] if len(estrazioni) >= 100 else estrazioni

    freq_50 = Counter()
    freq_100 = Counter()

    for estr in ultime_50:
        freq_50.update(estr)

    for estr in ultime_100:
        freq_100.update(estr)

    punteggi = {}

    for numero in range(1, 91):
        punteggio = (freq_50[numero] * 2) + (freq_100[numero] * 1)
        punteggi[numero] = punteggio

    return punteggi

# ================================
# CALCOLO RITARDI
# ================================
def calcola_ritardi(estrazioni):
    ritardi = {}
    totale = len(estrazioni)

    for numero in range(1, 91):
        ritardo = 0
        for i in range(totale - 1, -1, -1):
            if numero in estrazioni[i]:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    return ritardi

# ================================
# COMBINAZIONI INTELLIGENTI
# ================================
def genera_combinazioni(caldi, freddi, medi, ritardatari):
    combinazioni = []

    for _ in range(3):
        combo = set()

        if caldi:
            combo.add(random.choice(caldi))
        if freddi:
            combo.add(random.choice(freddi))
        if medi:
            combo.add(random.choice(medi))
        if ritardatari:
            combo.add(random.choice(ritardatari))

        while len(combo) < 5:
            combo.add(random.randint(1, 90))

        combinazioni.append(sorted(list(combo)))

    return combinazioni

# ================================
# API PRINCIPALE
# ================================
@app.route("/api")
def api():
    try:
        dati = carica_dati()
        risultato = []
        ruota_piu_forte = None
        pressione_massima = 0

        for ruota, estrazioni in dati.items():
            if len(estrazioni) == 0:
                continue

            punteggi = calcola_punteggi(estrazioni)
            ritardi = calcola_ritardi(estrazioni)

            ordinati = sorted(punteggi.items(), key=lambda x: x[1], reverse=True)

            numeri_caldi = [x[0] for x in ordinati[:3]]
            numeri_freddi = [x[0] for x in ordinati[-3:]]

            valori_medi = ordinati[20:40]
            numeri_medi = [x[0] for x in valori_medi[:10]]

            top_ritardi = sorted(ritardi.items(), key=lambda x: x[1], reverse=True)
            numeri_ritardatari = [x[0] for x in top_ritardi[:5]]

            indice_pressione = sum([punteggi[n] for n in numeri_caldi]) / 3

            if indice_pressione > pressione_massima:
                pressione_massima = indice_pressione
                ruota_piu_forte = ruota

            combinazioni = genera_combinazioni(
                numeri_caldi,
                numeri_freddi,
                numeri_medi,
                numeri_ritardatari
            )

            risultato.append({
                "ruota": ruota,
                "ultima_estrazione": estrazioni[-1],
                "numeri_caldi": numeri_caldi,
                "numeri_freddi": numeri_freddi,
                "ritardo_massimo": top_ritardi[0][1],
                "indice_pressione": round(indice_pressione, 2),
                "combinazioni_suggerite": combinazioni
            })

        return jsonify({
            "ruote": risultato,
            "ruota_piu_forte": ruota_piu_forte
        })

    except Exception as e:
        return jsonify({"errore": str(e)})

# ================================
# AVVIO SERVER
# ================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

























        











