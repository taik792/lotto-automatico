import json
from statistics import mean
from collections import Counter

# CONFIG
WINDOW_CICLO = 60
WINDOW_FREQ = 30

# CARICA DATI
with open("estrazioni.json") as f:
    estrazioni = json.load(f)

# ------------------------
# FUNZIONI
# ------------------------

def frequenza_numeri(estrazioni):
    flat = [n for e in estrazioni[-WINDOW_FREQ:] for n in e]
    return Counter(flat)

def ciclo_numero(estrazioni, numero):
    estr = estrazioni[-WINDOW_CICLO:]
    pos = []

    for i, e in enumerate(estr):
        if numero in e:
            pos.append(i)

    if len(pos) < 2:
        return 0

    cicli = [pos[i] - pos[i-1] for i in range(1, len(pos))]
    ciclo_medio = mean(cicli)
    ciclo_attuale = len(estr) - pos[-1]

    if ciclo_medio == 0:
        return 0

    return round(ciclo_attuale / ciclo_medio, 2)

def trova_caldi(estrazioni):
    freq = frequenza_numeri(estrazioni)
    return [n for n, _ in freq.most_common(2)]

# ------------------------
# MOTORE PRO
# ------------------------

risultati = {}

for ruota, estr in estrazioni.items():

    ultima = estr[-1]

    caldi = trova_caldi(estr)

    # ciclo per numeri caldi
    ciclo = [ciclo_numero(estr, n) for n in caldi]

    # indice = mix freq + ciclo
    freq = frequenza_numeri(estr)

    indice = []
    for n in caldi:
        f = freq.get(n, 0)
        c = ciclo_numero(estr, n)
        indice.append(round(f * 0.2 + c * 2, 2))

    # saturazione = media frequenze
    sat = mean([freq.get(n,0) for n in caldi]) / 10

    # 🔥 SCORE PRO
    score = (
        sum(indice) * 0.5 +
        sum(ciclo) * 1.5 +
        (freq.get(caldi[0],0) + freq.get(caldi[1],0)) * 0.1
        - sat
    )

    risultati[ruota] = {
        "ruota": ruota,
        "ultima": ultima,
        "caldi": caldi,
        "ambo": caldi,
        "ciclo": ciclo,
        "indice": indice,
        "saturazione": round(sat,2),
        "score": round(score,2)
    }

# ------------------------
# SALVA
# ------------------------

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)

print("🔥 MOTORE PRO ATTIVO")