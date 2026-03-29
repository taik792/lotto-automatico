import json
from statistics import mean
from datetime import datetime

# CONFIG
WINDOW_CICLO = 60
WINDOW_FREQ = 30
WINDOW_RECENTE = 10

# CARICA DATI
with open("estrazioni.json") as f:
    estrazioni = json.load(f)

# CARICA STORICO
try:
    with open("storico.json") as f:
        storico = json.load(f)
except:
    storico = []

# FUNZIONI
def frequenza(estrazioni, numero):
    return sum(numero in e for e in estrazioni[-WINDOW_FREQ:])

def ciclometria(estrazioni, numero):
    estr = estrazioni[-WINDOW_CICLO:]
    pos = [i for i,e in enumerate(estr) if numero in e]

    if len(pos) < 2:
        return 0

    cicli = [pos[i] - pos[i-1] for i in range(1,len(pos))]
    ciclo_medio = mean(cicli)
    ciclo_attuale = len(estr) - pos[-1]

    if ciclo_medio == 0:
        return 0

    return round(ciclo_attuale / ciclo_medio, 2)

def indice(estrazioni, numero):
    freq = frequenza(estrazioni, numero)
    recente = sum(numero in e for e in estrazioni[-WINDOW_RECENTE:])
    return round(freq * 0.7 + recente * 1.3, 2)

# CALCOLO
risultati = {}

for ruota, estr in estrazioni.items():

    numeri = range(1, 91)

    score_numeri = []

    for n in numeri:
        ind = indice(estr, n)
        ciclo = ciclometria(estr, n)

        score = ind * 0.6 + ciclo * 0.4
        score_numeri.append((n, score))

    # TOP NUMERI
    top = sorted(score_numeri, key=lambda x: x[1], reverse=True)[:6]
    numeri_top = [n for n,_ in top]

    # CREA AMBO MIGLIORE
    ambo = numeri_top[:2]

    # SCORE FINALE
    score_finale = round(sum([s for _,s in top[:2]]),2)

    risultati[ruota] = {
        "ruota": ruota,
        "ultima": estr[-1],
        "caldi": numeri_top[:2],
        "ambo": ambo,
        "score": score_finale
    }

# SALVA RISULTATI
with open("risultati.json","w") as f:
    json.dump(risultati, f, indent=2)

# 🔥 SALVA STORICO (ELITE)
oggi = datetime.now().strftime("%Y-%m-%d")

for r in risultati.values():
    storico.append({
        "data": oggi,
        "ruota": r["ruota"],
        "ambo": r["ambo"],
        "score": r["score"]
    })

with open("storico.json","w") as f:
    json.dump(storico, f, indent=2)

print("ELITE attivo ✔")