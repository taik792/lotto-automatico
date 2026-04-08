import json
import os
from collections import defaultdict

TOP_NUMERI = 12
AMBI_FINALI = 20

PESO_FREQ = 2.0
PESO_SCORE = 1.5
PESO_RITARDO = 0.3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_estrazioni = os.path.join(BASE_DIR, "estrazioni.json")
file_output = os.path.join(BASE_DIR, "risultati.json")

# ======================
# CARICA DATI PER RUOTA
# ======================
with open(file_estrazioni, "r") as f:
    estrazioni_raw = json.load(f)

estrazioni_per_ruota = {}

for ruota, estrazioni in estrazioni_raw.items():
    estrazioni_per_ruota[ruota] = estrazioni[::-1]  # recenti prima

# ======================
# ULTIME ESTRAZIONI 🔥
# ======================
ultime_estrazioni = {}

for ruota, estrazioni in estrazioni_per_ruota.items():
    if estrazioni:
        ultime_estrazioni[ruota] = estrazioni[0]

# ======================
# UNISCI TUTTE LE ESTRAZIONI
# ======================
estrazioni = []

for ruota in estrazioni_per_ruota.values():
    estrazioni.extend(ruota)

# ======================
# RITARDI
# ======================
ritardi = {i: 0 for i in range(1, 91)}

for numero in range(1, 91):
    for idx, estr in enumerate(estrazioni):
        if numero in estr:
            ritardi[numero] = idx
            break

# ======================
# FREQUENZE
# ======================
freq_num = defaultdict(int)

for estr in estrazioni[:100]:
    for n in estr:
        freq_num[n] += 1

# ======================
# SCORE
# ======================
score_num = {}

for n in range(1, 91):
    score_num[n] = freq_num[n] * 1.2 + ritardi[n] * 0.8

# ======================
# COPPIE
# ======================
freq_coppie = defaultdict(lambda: defaultdict(int))

for estr in estrazioni[:150]:
    for i in range(len(estr)):
        for j in range(i + 1, len(estr)):
            a, b = estr[i], estr[j]
            freq_coppie[a][b] += 1
            freq_coppie[b][a] += 1

# ======================
# TOP NUMERI
# ======================
ranking = sorted(score_num.items(), key=lambda x: x[1], reverse=True)
top_numbers = [n for n, _ in ranking[:TOP_NUMERI]]

# ======================
# GENERA AMBI
# ======================
ambi = []

for n1 in top_numbers:
    best_score = -1
    best_n2 = None

    for n2 in top_numbers:
        if n1 == n2:
            continue

        score = (
            freq_coppie[n1][n2] * PESO_FREQ +
            score_num[n2] * PESO_SCORE +
            ritardi[n2] * PESO_RITARDO
        )

        if score > best_score:
            best_score = score
            best_n2 = n2

    if best_n2:
        ambo = sorted([n1, best_n2])

        if ambo not in [a["ambo"] for a in ambi]:
            ambi.append({
                "ambo": ambo,
                "score": round(best_score, 2)
            })

# ======================
# LIMITA RIPETIZIONI
# ======================
conteggio = {}
filtrati = []

for item in ambi:
    n1, n2 = item["ambo"]

    if conteggio.get(n1, 0) >= 3:
        continue
    if conteggio.get(n2, 0) >= 3:
        continue

    filtrati.append(item)

    conteggio[n1] = conteggio.get(n1, 0) + 1
    conteggio[n2] = conteggio.get(n2, 0) + 1

ambi = filtrati

# ======================
# ORDINA
# ======================
ambi.sort(key=lambda x: x["score"], reverse=True)
ambi = ambi[:AMBI_FINALI]

top = ambi[:3]

# ======================
# SALVA OUTPUT
# ======================
output = {
    "ultime_estrazioni": ultime_estrazioni,
    "top": top,
    "ambi": ambi
}

with open(file_output, "w") as f:
    json.dump(output, f, indent=2)

print("✅ risultati aggiornati con ruote")