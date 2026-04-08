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

estrazioni_per_ruota = {}

for ruota, estrazioni in estrazioni_raw.items():
    estrazioni_per_ruota[ruota] = estrazioni[::-1]

# ======================
# ULTIME ESTRAZIONI
# ======================
ultime = {r: e[0] for r, e in estrazioni_per_ruota.items() if e}

# ======================
# FREQUENZE PER RUOTA
# ======================
freq_ruota = {}

for ruota, estrazioni in estrazioni_per_ruota.items():
    freq = defaultdict(int)

    for estr in estrazioni[:100]:
        for n in estr:
            freq[n] += 1

    freq_ruota[ruota] = freq

# ======================
# RUOTE GEMELLE
# ======================
def similarita(f1, f2):
    return sum(min(f1[n], f2[n]) for n in range(1, 91))

ruota_gemella = {}

ruote = list(freq_ruota.keys())

for r1 in ruote:
    best = None
    best_score = -1

    for r2 in ruote:
        if r1 == r2:
            continue

        score = similarita(freq_ruota[r1], freq_ruota[r2])

        if score > best_score:
            best_score = score
            best = r2

    ruota_gemella[r1] = best

# ======================
# UNIONE ESTRAZIONI
# ======================
estrazioni = []

for e in estrazioni_per_ruota.values():
    estrazioni.extend(e)

# ======================
# RITARDI
# ======================
ritardi = {i: 0 for i in range(1, 91)}

for n in range(1, 91):
    for idx, estr in enumerate(estrazioni):
        if n in estr:
            ritardi[n] = idx
            break

# ======================
# FREQUENZE GLOBALI
# ======================
freq = defaultdict(int)

for estr in estrazioni[:100]:
    for n in estr:
        freq[n] += 1

# ======================
# COPPIE
# ======================
freq_coppie = defaultdict(lambda: defaultdict(int))

for estr in estrazioni[:150]:
    for i in range(len(estr)):
        for j in range(i+1, len(estr)):
            a, b = estr[i], estr[j]
            freq_coppie[a][b] += 1
            freq_coppie[b][a] += 1

# ======================
# SCORE NUMERI
# ======================
score_num = {}

for n in range(1, 91):
    score_num[n] = freq[n]*1.2 + ritardi[n]*0.8

# ======================
# AMBI
# ======================
ambi = []

for n1 in range(1, 91):
    best = None
    best_score = 0

    for n2 in range(1, 91):
        if n1 == n2:
            continue

        score = freq_coppie[n1][n2]*2 + score_num[n2]

        if score > best_score:
            best_score = score
            best = n2

    if best:
        ambi.append({
            "numeri": sorted([n1, best]),
            "raw": best_score
        })

# ======================
# NORMALIZZA
# ======================
max_score = max(a["raw"] for a in ambi)

for a in ambi:
    a["prob"] = round((a["raw"] / max_score) * 100, 2)

ambi.sort(key=lambda x: x["prob"], reverse=True)

top_ambi = ambi[:2]

# ======================
# TERNI
# ======================
terni = []

for a in top_ambi:
    n1, n2 = a["numeri"]

    best_n3 = None
    best_score = 0

    for n3 in range(1, 91):
        if n3 in [n1, n2]:
            continue

        score = (
            freq_coppie[n1][n3] +
            freq_coppie[n2][n3] +
            score_num[n3]
        )

        if score > best_score:
            best_score = score
            best_n3 = n3

    if best_n3:
        terni.append({
            "numeri": sorted([n1, n2, best_n3]),
            "prob": round((best_score / max_score) * 100, 2)
        })

# ======================
# OUTPUT
# ======================
output = {
    "ultime_estrazioni": ultime,
    "ruote_gemelle": ruota_gemella,
    "top_ambi": top_ambi,
    "top_terni": terni
}

with open(file_output, "w") as f:
    json.dump(output, f, indent=2)

print("✅ VERSIONE COMPATTA ATTIVA")