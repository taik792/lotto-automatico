import json
from statistics import mean

WINDOW_CICLO = 60
WINDOW_FREQ = 30
WINDOW_RECENTE = 10

with open("estrazioni.json") as f:
    estrazioni = json.load(f)

def ciclometria(estrazioni, numero):
    estrazioni = estrazioni[-WINDOW_CICLO:]

    pos = []
    for i, estr in enumerate(estrazioni):
        if numero in estr:
            pos.append(i)

    if len(pos) < 2:
        return 0

    cicli = [pos[i] - pos[i-1] for i in range(1, len(pos))]
    ciclo_medio = mean(cicli)

    ciclo_attuale = len(estrazioni) - pos[-1]

    return round(ciclo_attuale / ciclo_medio, 2)

def frequenza(estrazioni, numero):
    estrazioni = estrazioni[-WINDOW_FREQ:]
    count = sum(1 for estr in estrazioni if numero in estr)
    return count / len(estrazioni)

def recente(estrazioni, numero):
    estrazioni = estrazioni[-WINDOW_RECENTE:]
    return sum(1 for estr in estrazioni if numero in estr)

def indice(numero, estrazioni):
    f = frequenza(estrazioni, numero)
    c = ciclometria(estrazioni, numero)
    r = recente(estrazioni, numero)

    # formula migliorata
    score = (c * 1.5) + (f * 10) + (r * 0.5)
    return round(score, 2)

def saturazione(estrazioni):
    return round(len