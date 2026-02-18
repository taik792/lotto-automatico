from flask import Flask, jsonify
import json
import random
from collections import Counter

app = Flask(__name__)

WINDOW_CALDI = 50
WINDOW_MEDI = 100

def carica_dati():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

def calcola_statistiche(ruota, estrazioni):

    if len(estrazioni) < 5:
        return None

    numeri_totali = list(range(1, 91))

    # -----------------------------
    # FLATTEN ESTRAZIONI
    # -----------------------------
    tutte = [n for e in estrazioni for n in e]
    ultime50 = [n for e in estrazioni[-WINDOW_CALDI:] for n in e]
    ultime100 = [n for e in estrazioni[-WINDOW_MEDI:] for n in e]

    freq_tot = Counter(tutte)
    freq_50 = Counter(ultime50)
    freq_100 = Counter(ultime100)

    # -----------------------------
    # CALDI / FREDDI
    # -----------------------------
    caldi = [n for n, _ in freq_50.most_common(3)]

    freddi = sorted(numeri_totali, key=lambda x: freq_50.get(x, 0))[:3]

    # -----------------------------
    # RITARDI
    # -----------------------------
    ritardi = {}
    for n in numeri_totali:
        ritardo = 0
        for estr in reversed(estrazioni):
            if n in estr:
                break
            ritardo += 1
        ritardi[n] = ritardo

    ritardatario = max(ritardi, key=ritardi.get)
    ritardo_max = ritardi[ritardatario]

    top5_ritardi = sorted(ritardi.values(), reverse=True)[:5]
    media_top5 = sum(top5_ritardi) / 5

    # -----------------------------
    # INDICE PRESSIONE PONDERATO
    # -----------------------------
    pressione = (
        (ritardo_max * 0.5) +
        (media_top5 * 0.3) +
        ((1 / (sum(freq_100.values()) / len(numeri_totali))) * 0.2)
    )

    pressione = round(pressione, 2)

    # -----------------------------
    # NUMERI SUGGERITI BILANCIATI
    # -----------------------------
    medi = sorted(numeri_totali, key=lambda x: abs(freq_100.get(x, 0) - 5))[:10]

    suggerite = []

    for _ in range(3):
        combo = []
        combo += random.sample(caldi, min(2, len(caldi)))
        combo.append(ritardatario)
        combo += random.sample(medi, 2)
        combo = sorted(set(combo))
        suggerite.append(combo[:5])

    # -----------------------------
    # MODALITÀ AGGRESSIVA
    # -----------------------------
    top_rit = sorted(ritardi, key=ritardi.get, reverse=True)[:5]

    aggressive = []
    for _ in range(2):
        combo = []
        combo += random.sample(top_rit, 3)
        combo += random.sample(caldi, 1)
        combo += random.sample(numeri_totali, 1)
        combo = sorted(set(combo))
        aggressive.append(combo[:5])

    return {
        "ruota": ruota,
        "ultima_estrazione": estrazioni[-1],
        "numeri_caldi": caldi,
        "numeri_freddi": freddi,
        "ritardatario": ritardatario,
        "ritardo_massimo": ritardo_max,
        "indice_pressione": pressione,
        "combinazioni_bilanciate": suggerite,
        "combinazioni_aggressive": aggressive
    }


@app.route("/api")
def api():
    try:
        dati = carica_dati()
        risultato = []

        for ruota, estrazioni in dati.items():
            stats = calcola_statistiche(ruota, estrazioni)
            if stats:
                risultato.append(stats)

        if not risultato:
            return jsonify({"errore": "Dati insufficienti"})

        ruota_forte = max(risultato, key=lambda x: x["indice_pressione"])

        return jsonify({
            "ruota_piu_forte": ruota_forte["ruota"],
            "dati": risultato
        })

    except Exception as e:
        return jsonify({"errore": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


























        











