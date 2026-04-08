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
# UNIONE ESTRAZIONI
# ======================
estrazioni = []
for e in estrazioni_per_ruota.values():
    estrazioni.extend(e)

# ======================
# FREQUENZE GLOBALI
# ======================
freq = defaultdict(int)

for estr in estrazioni[:120]:
    for n in estr:
        freq[n] += 1

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
score_num = {
    n: freq[n]*1.2 + ritardi[n]*0.8
    for n in range(1, 91)
}

# ======================
# GENERA AMBI (BILANCIATI)
# ======================
ambi = []

for n1 in range(1, 91):
    for n2 in range(n1+1, 91):

        score = (
            freq_coppie[n1][n2]*2 +
            score_num[n1] +
            score_num[n2]
        )

        ambi.append({
            "numeri": [n1, n2],
            "score": score
        })

# ORDINA
ambi.sort(key=lambda x: x["score"], reverse=True)

# ======================
# FILTRO INTELLIGENTE
# ======================
finali = []
uso_numeri = defaultdict(int)

for a in ambi:
    n1, n2 = a["numeri"]

    # max 2 volte lo stesso numero
    if uso_numeri[n1] >= 2 or uso_numeri[n2] >= 2:
        continue

    finali.append(a)

    uso_numeri[n1] += 1
    uso_numeri[n2] += 1

    if len(finali) == 3:
        break

# ======================
# ASSEGNA RUOTA MIGLIORE
# ======================
top = []

for a in finali:
    best_ruota = None
    best_score = -1

    for r, estr in estrazioni_per_ruota.items():

        freq_r = defaultdict(int)
        for e in estr[:80]:
            for n in e:
                freq_r[n] += 1

        score = freq_r[a["numeri"][0]] + freq_r[a["numeri"][1]]

        if score > best_score:
            best_score = score
            best_ruota = r

    a["ruota"] = best_ruota
    top.append(a)

# ======================
# PROBABILITÀ
# ======================
max_score = max(a["score"] for a in top)

for a in top:
    a["prob"] = round((a["score"] / max_score) * 100, 2)

# ======================
# RUOTA GEMELLA (JOLLY)
# ======================
freq_ruota = {}

for r, estr in estrazioni_per_ruota.items():
    f = defaultdict(int)
    for e in estr[:80]:
        for n in e:
            f[n] += 1
    freq_ruota[r] = f

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

ruota_jolly = ruota_gemella[top[0]["ruota"]]

# ======================
# OUTPUT
# ======================
output = {
    "ultime_estrazioni": ultime,
    "top_ambi": top,
    "ruota_jolly": ruota_jolly
}

with open(file_output, "w") as f:
    json.dump(output, f, indent=2)

print("✅ SISTEMA BILANCIATO ATTIVO")