import json
from collections import Counter

FINESTRA = 200  # cambia qui se vuoi (100 / 200 / 300)


# =========================
# CICLOMETRIA VERA (RITARDO)
# =========================
def calcola_ritardi(estrazioni):
    ritardi = {n: None for n in range(1, 91)}

    for i, estrazione in enumerate(estrazioni):
        for numero in estrazione:
            if ritardi[numero] is None:
                ritardi[numero] = i

    for n in ritardi:
        if ritardi[n] is None:
            ritardi[n] = len(estrazioni)

    return ritardi


# =========================
# SATURAZIONE
# =========================
def calcola_saturazione(numeri):
    freq = Counter(numeri)
    return round(sum(freq.values()) / len(freq), 2)


# =========================
# ANALISI SINGOLA RUOTA
# =========================
def analizza_ruota(nome, estrazioni):
    estrazioni = estrazioni[:FINESTRA]

    ultima = estrazioni[0]

    numeri = [n for e in estrazioni for n in e]