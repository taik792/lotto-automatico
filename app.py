import json
from collections import Counter
from itertools import combinations

# -------------------------
# PARAMETRI
# -------------------------

NUMERI_RUOTA = 5
MAX_NUMERO = 90

ULTIME_ESTRAZIONI = 24
TOP_NUMERI = 4
NUMERI_FINALI = 2


# -------------------------
# CARICA DATI
# -------------------------

with open("estrazioni.json", "r") as f:
    data = json.load(f)

ruote = data.keys()


# -------------------------
# FREQUENZA NUMERI
# -------------------------

def calcola_frequenza(estrazioni):

    freq = Counter()

    for estr in estrazioni[-ULTIME_ESTRAZIONI:]:
        for n in estr:
            freq[n] += 1

    return freq


# -------------------------
# RITARDO NUMERI
# -------------------------

def calcola_ritardo(estrazioni):

    ritardi = {}

    ultime = estrazioni[-ULTIME_ESTRAZIONI:]

    for numero in range(1, MAX_NUMERO + 1):

        ritardo = 0

        for estr in reversed(ultime):

            if numero in estr:
                break

            ritardo += 1

        ritardi[numero] = ritardo

    return ritardi


# -------------------------
# SCORE NUMERI
# -------------------------

def score_numeri(freq, ritardi):

    score = {}

    for numero in range(1, MAX_NUMERO + 1):

        frequenza = freq.get(numero, 0)
        ritardo = ritardi.get(numero, 0)

        score[numero] = frequenza + ritardo

    return score


# -------------------------
# CONVERGENZA COPPIE
# -------------------------

def convergenza(estrazioni):

    coppie = Counter()

    for estr in estrazioni[-ULTIME_ESTRAZIONI:]:

        for c in combinations(sorted(estr), 2):
            coppie[c] += 1

    return coppie


# -------------------------
# ANALISI RUOTE
# -------------------------

risultati = []

for ruota in ruote:

    estrazioni = data[ruota]

    freq = calcola_frequenza(estrazioni)
    ritardi = calcola_ritardo(estrazioni)

    score = score_numeri(freq, ritardi)

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[:TOP_NUMERI]

    top_numeri = [n[0] for n in top]

    coppie = convergenza(estrazioni)

    migliori_coppie = []

    for c in combinations(top_numeri, 2):

        key = tuple(sorted(c))

        forza = coppie.get(key, 0)

        bonus = score.get(c[0], 0) + score.get(c[1], 0)

        forza_totale = forza * 2 + bonus

        migliori_coppie.append((c, forza_totale))

    migliori_coppie.sort(key=lambda x: x[1], reverse=True)

    numeri_finali = top_numeri[:NUMERI_FINALI]

    risultati.append({
        "ruota": ruota,
        "numeri": numeri_finali,
        "ambi_forti": migliori_coppie[:3]
    })


# -------------------------
# SALVA RISULTATI
# -------------------------

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)


print("Aggiornamento completato")
