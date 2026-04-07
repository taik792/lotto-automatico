import json
import random

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia"]

with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {
    "top": [],
    "ruote": {},
    "giocate": [],
    "jolly": {}
}

def calcola_freq(lista):
    freq = {}
    for estr in lista:
        for n in estr:
            freq[n] = freq.get(n, 0) + 1
    return freq

for ruota in RUOTE:

    if ruota not in estrazioni:
        continue

    estrazioni_ruota = estrazioni[ruota]

    if len(estrazioni_ruota) < 20:
        continue

    # ✔ ULTIMA (funziona perché hai ordine cronologico corretto)
    ultime = estrazioni_ruota[-1]

    breve = estrazioni_ruota[-20:]
    medio = estrazioni_ruota[-100:]
    lungo = estrazioni_ruota[-500:]

    freq_breve = calcola_freq(breve)
    freq_medio = calcola_freq(medio)
    freq_lungo = calcola_freq(lungo)

    # ritardi
    ritardi = {}
    for n in range(1, 91):
        ritardo = 0
        for estr in reversed(estrazioni_ruota):
            if n in estr:
                break
            ritardo += 1
        ritardi[n] = ritardo

    score_num = {}

    for n in range(1, 91):

        penalita = 10 if n in ultime else 0

        ultime_5 = estrazioni_ruota[-5:]
        pres