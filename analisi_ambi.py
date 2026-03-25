import json
from collections import Counter

# =========================
# PARAMETRI
# =========================
FINESTRA_ESTRAZIONI = 200  # puoi mettere 100 / 200 / 300

# =========================
# CICLOMETRIA VERA
# =========================
def calcola_ritardi(estrazioni_ruota):
    ritardi = {n: None for n in range(1, 91)}

    for i, estrazione in enumerate(estrazioni_ruota):
        for numero in estrazione:
            if ritardi[numero] is None:
                ritardi[numero] = i

    # se un numero non è mai uscito → metti valore alto
    for n in ritardi:
        if ritardi[n] is None:
            ritardi[n] = len(estrazioni_ruota)

    return ritardi

# =========================
# SATURAZIONE REALE
# =========================
def calcola_saturazione(numeri_ruota):
    freq = Counter(numeri_ruota)
    return round(sum(freq.values()) / len(freq), 2)

# =========================
# ANALISI RUOTA
# =========================
def analizza_ruota(nome_ruota, estrazioni):
    estrazioni = estrazioni[:FINESTRA_ESTRAZIONI]

    # ultima estrazione
    ultima = estr