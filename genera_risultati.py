import json
import os
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_estrazioni = os.path.join(BASE_DIR, "estrazioni.json")
file_output = os.path.join(BASE_DIR, "risultati.json")

# ======================
# CARICA DATI
# ======================
with open(file_estrazioni, "r") as f:
    estrazioni_raw = json.load(f)

estrazioni_per_ruota = {
    r: e[::-1] for r, e in estrazioni_raw.items()
}

ultime = {r: e[0] for r, e in estrazioni_per_ruota.items() if e}

# ======================
# FREQUENZE PER RUOTA
# ======================
freq_ruota = {}

for r, estr in estrazioni_per_ruota.items():
    f = defaultdict(int)
    for e in estr[:100]:
        for n in e:
            f[n] += 1
    freq_ruota[r] = f

# ======================
# RUOTE GEMELLE
# ======================
def similarita(f1, f2):
    return sum(min(f1[n], f2[n]) for n in range(1, 91))

ruota_gemella = {}

for r1 in freq_ruota:
    best = None
    best_score = -1

    for r2 in freq_ruota:
        if r1 == r2:
            continue

        s = similarita(freq_ruota[r1], freq_ruota[r2])

        if s > best_score:
            best_score = s
            best = r2

    ruota_gemella[r1] = best

# ======================
# GENERA AMBI PER RUOTA
# ======================
candidati = []

for r, estr in estrazioni_per_ruota.items():

    freq = defaultdict(int)
    for e in estr[:100]:
        for n in e:
            freq[n] += 1

    for n1 in range(1, 91):
        for n2 in range(n1+1, 91):

            score = freq[n1] + freq[n2]

            candidati.append({
                "ruota": r,
                "numeri": [n1, n2],
                "score": score
            })

# ======================
# ORDINA
# ======================
candidati.sort(key=lambda x: x["score"], reverse=True)

# ======================
# FILTRO FORTE
# ======================
top = []
numeri_usati = set()
ruote_usate = set()

for c in candidati:

    n1, n2 = c["numeri"]
    r = c["ruota"]

    if n1 in numeri_usati or n2 in numeri_usati:
        continue

    if r in ruote_usate:
        continue

    top.append(c)

    numeri_usati.add(n1)
    numeri_usati.add(n2)
    ruote_usate.add(r)

    if len(top) == 3:
        break

# ======================
# PROBABILITÀ
# ======================
max_score = max(c["score"] for c in top)

for c in top:
    c["prob"] = round((c["score"] / max_score) * 100, 2)

# ======================
# RUOTA JOLLY
# ======================
ruota_top = top[0]["ruota"]
ruota_jolly = ruota_gemella[ruota_top]

# ======================
# OUTPUT
# ======================
output = {
    "ultime_estrazioni": ultime,
    "top": top,
    "ruota_jolly": ruota_jolly
}

with open(file_output, "w") as f:
    json.dump(output, f, indent=2)

print("✅ VERSIONE STRATEGICA ATTIVA")