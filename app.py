import json
from collections import Counter
from itertools import combinations

# -----------------------------
# PARAMETRI
# -----------------------------

NUMERI_RUOTA = 5
MAX_NUMERO = 90
ULTIME_ESTRAZIONI = 24
TOP_NUMERI = 4
NUMERI_FINALI = 2

# -----------------------------
# CARICA DATI JSON
# -----------------------------

with open("estrazioni.json", "r") as f:
    data = json.load(f)

ruote = data.keys()

# -----------------------------
# FUNZIONE CALCOLO FREQUENZA
# -----------------------------

def calcola_frequenza(estrazioni):
    freq = Counter()
    for estr in estrazioni[-ULTIME_ESTRAZIONI:]:
        for n in estr:
            freq[n] += 1
    return freq

# -----------------------------
# CALCOLO RITARDO
# -----------------------------

def calcola_ritardo(estrazioni):
    ritardi = {}
    for numero in range(1, MAX_NUMERO + 1):
        ritardo = 0
        for estr in reversed(estrazioni):
            if numero in estr:
                break
            ritardo += 1
        ritardi[numero] = ritardo
    return ritardi

# -----------------------------
# SCORE NUMERI
# -----------------------------

def score_numeri(freq, ritardi):

    score = {}

    for n in range(1, MAX_NUMERO + 1):

        f = freq.get(n, 0)
        r = ritardi.get(n, 0)

        score[n] = (f * 2) + r

    return score

# -----------------------------
# FILTRO CONVERGENZA
# -----------------------------

def convergenza(estrazioni):

    coppie = Counter()

    for estr in estrazioni[-ULTIME_ESTRAZIONI:]:
        for c in combinations(estr, 2):
            coppie[tuple(sorted(c))] += 1

    return coppie

# -----------------------------
# ANALISI RUOTE
# -----------------------------

risultati = []

for ruota in ruote:

    estrazioni = data[ruota]

    freq = calcola_frequenza(estrazioni)
    ritardi = calcola_ritardo(estrazioni)

    score = score_numeri(freq, ritardi)

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[:TOP_NUMERI]

    top_numeri = [n[0] for n in top]

    # convergenza
    coppie = convergenza(estrazioni)

    migliori_coppie = []

    for c in combinations(top_numeri, 2):

        key = tuple(sorted(c))
        forza = coppie.get(key, 0)

        migliori_coppie.append((c, forza))

    migliori_coppie.sort(key=lambda x: x[1], reverse=True)

    numeri_finali = top_numeri[:NUMERI_FINALI]

    risultati.append({
        "ruota": ruota,
        "numeri": numeri_finali,
        "ambi_forti": migliori_coppie[:3]
    })

# -----------------------------
# ORDINA MIGLIORI RUOTE
# -----------------------------

print("\nPREVISIONI LOTTO EVOLUTION PRO MAX 2.0\n")

for r in risultati:

    print("Ruota:", r["ruota"])
    print("Numeri:", r["numeri"])

    print("Ambi forti:")
    for a in r["ambi_forti"]:
        print(" ", a)

    print("-" * 40)
