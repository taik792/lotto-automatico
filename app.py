import json
from collections import Counter
from itertools import combinations

ULTIME_ESTRAZIONI = 24
TOP_NUMERI = 4
NUMERI_FINALI = 2
MAX_NUMERO = 90


with open("estrazioni.json") as f:
    data = json.load(f)

ruote = data.keys()


def frequenza(estrazioni):

    freq = Counter()

    for estr in estrazioni[-ULTIME_ESTRAZIONI:]:
        for n in estr:
            freq[n] += 1

    return freq


def ritardi(estrazioni):

    rit = {}

    for n in range(1, MAX_NUMERO + 1):

        r = 0

        for estr in reversed(estrazioni):

            if n in estr:
                break

            r += 1

        rit[n] = r

    return rit


def score_numeri(freq, rit):

    score = {}

    for n in range(1, MAX_NUMERO + 1):

        score[n] = freq.get(n, 0) + rit.get(n, 0)

    return score


def convergenza(estrazioni):

    coppie = Counter()

    for estr in estrazioni[-ULTIME_ESTRAZIONI:]:

        for c in combinations(sorted(estr), 2):
            coppie[c] += 1

    return coppie


risultati = []

for ruota in ruote:

    estrazioni = data[ruota]

    freq = frequenza(estrazioni)
    rit = ritardi(estrazioni)

    score = score_numeri(freq, rit)

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[:TOP_NUMERI]

    top_numeri = [x[0] for x in top]

    coppie = convergenza(estrazioni)

    ambi = []

    for c in combinations(top_numeri, 2):

        key = tuple(sorted(c))

        forza = coppie.get(key, 0)

        bonus = score[c[0]] + score[c[1]]

        totale = forza * 2 + bonus

        ambi.append((c, totale))

    ambi.sort(key=lambda x: x[1], reverse=True)

    risultati.append({
        "ruota": ruota,
        "numeri": top_numeri[:NUMERI_FINALI],
        "ambi": ambi[:3]
    })


with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)

print("Aggiornamento completato")
