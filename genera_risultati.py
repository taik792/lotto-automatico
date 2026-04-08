import json
import random
from itertools import combinations

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia","Nazionale"]

BREVE = 20
MEDIO = 80
LUNGO = 200

with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {"top": [], "ruote": {}, "giocate": [], "jolly": {}}

def freq(lista):
    f = {}
    for e in lista:
        for n in e:
            f[n] = f.get(n, 0) + 1
    return f

# ===== ANALISI =====
for ruota in RUOTE:

    if ruota not in estrazioni:
        continue

    data = estrazioni[ruota]
    ultime = data[-1]

    breve = data[-BREVE:]
    medio = data[-MEDIO:]
    lungo = data[-LUNGO:]

    fb, fm, fl = freq(breve), freq(medio), freq(lungo)

    # ritardi
    ritardi = {}
    for n in range(1,91):
        r = 0
        for e in reversed(data):
            if n in e:
                break
            r +=