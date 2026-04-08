import json
import os
from collections import defaultdict

# ================================
# CONFIG
# ================================
TOP_NUMERI = 12
AMBI_FINALI = 20

PESO_FREQ = 2.0
PESO_SCORE = 1.5
PESO_RITARDO = 0.3

# ================================
# PATH
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_estrazioni = os.path.join(BASE_DIR, "estrazioni.json")
file_output = os.path.join(BASE_DIR, "risultati.json")

# ================================
# CARICA ESTRAZIONI (ROBUSTO)
# ================================
with open(file_estrazioni, "r") as f:
    estrazioni_raw = json.load(f)

estrazioni = []

# 🔥 supporta sia dict che lista
if isinstance(estrazioni_raw, dict):
    for ruota in estrazioni_raw.values():
        estrazioni.extend(ruota)
else:
    estrazioni = estrazioni_raw

# 🔥 inverti (recenti prima)
estrazioni = estrazioni[::-1]

# ================================
# CALCOLO RITARDI
# ================================
ritardi = {i: 0 for i in range(1, 91)}

for numero in range(1, 91):
    for idx, estr in enumerate(estrazioni):
        if numero in estr:
            ritardi[numero] = idx
            break

# ================================
# FREQUENZA NUMERI
# ================================
freq_num = defaultdict(int)

for estr in estrazioni[:100]:
    for n in estr:
        freq_num[n] += 1

# ================================
# SCORE NUMERI
# ================================
score_num = {}

for n in range(1, 91):
    score_num[n] = (
        freq_num[n] * 1.2 +
        ritardi[n] * 0.8
    )

# ================================
# FREQUENZA COPPIE
# ================================
freq_coppie = defaultdict(lambda: defaultdict(int))

for estr in estrazioni[:150]:
    for i in range(len(estr)):
        for j in range(i + 1, len(estr)):
            a, b = estr[i], estr[j]
            freq_coppie[a][b] += 1
            freq_coppie[b][a] += 1

# ================================
# NUMERI TOP
# ================================
ranking = sorted(score_num.items(), key=lambda x: x[1], reverse=True)
top_numbers = [n for n, _ in ranking[:TOP_NUMERI]]

# ================================
# GENERA AMBI INTELLIGENTI
# ================================
ambi = []

for n1 in top_numbers:

    best_score = -1
    best_n2 = None

    for n2 in top_numbers:
        if n1 == n2:
            continue

        freq = freq_coppie[n1][n2]

        score = (
            freq * PESO_FREQ +
            score_num[n2] * PESO_SCORE +
            ritardi[n2] * PESO_RITARDO
        )

        if score > best_score:
            best_score = score
            best_n2 = n2

    if best_n2:
        ambo = sorted([n1, best_n2])

        # evita duplicati
        if ambo not in [a["ambo"] for a in ambi]:
            ambi.append({
                "ambo": ambo,
                "score": round(best_score, 4)
            })

# ================================
# ORDINA E TAGLIA
# ================================
ambi.sort(key=lambda x: x["score"], reverse=True)
ambi = ambi[:AMBI_FINALI]

# ================================
# SALVA JSON (FORMATO SITO)
# ================================
with open(file_output, "w") as f:
    json.dump(ambi, f, indent=2)

print("✅ risultati.json aggiornato correttamente")