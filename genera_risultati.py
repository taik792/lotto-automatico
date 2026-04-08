import json
from collections import Counter

# ⚙️ CONFIG
LUNGO = 500
MEDIO = 200
BREVE = 50

PESO_LUNGO = 1
PESO_MEDIO = 2
PESO_BREVE = 3

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia"]

GEMELLE = {
    "Bari": "Cagliari",
    "Cagliari": "Bari",
    "Firenze": "Genova",
    "Genova": "Firenze",
    "Milano": "Napoli",
    "Napoli": "Milano",
    "Palermo": "Roma",
    "Roma": "Palermo",
    "Torino": "Venezia",
    "Venezia": "Torino"
}


# 📥 carica estrazioni
with open("estrazioni.json") as f:
    data = json.load(f)

estrazioni = data[-LUNGO:]  # prendiamo ultime N


# 🔢 calcolo ritardi
def calcola_ritardi(ruota, window):
    ritardi = {n: 0 for n in range(1, 91)}

    subset = estrazioni[-window:]

    for numero in range(1, 91):
        ritardo = 0
        for estr in reversed(subset):
            if numero in estr[ruota]:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    return ritardi


# 🔗 frequenze coppie
def frequenze_coppie(ruota):
    c = Counter()
    for estr in estrazioni:
        nums = sorted(estr[ruota])
        for i in range(len(nums)):
            for j in range(i+1, len(nums