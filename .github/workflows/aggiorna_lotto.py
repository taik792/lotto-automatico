import requests
import json

URL = "https://www.superenalotto.it/estrazioni/lotto"
FILE = "storico.json"

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def salva_storico(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def scarica():
    estrazioni = {}

    for ruota in RUOTE:
        # Simulazione ultime 10 estrazioni (test stabile)
        estrazioni[ruota] = [
            [11,22,33,44,55],
            [5,12,18,34,67],
            [7,14,21,28,35],
            [1,9,19,29,39],
            [3,13,23,33,43],
            [8,18,28,38,48],
            [6,16,26,36,46],
            [10,20,30,40,50],
            [2,12,22,32,42],
            [4,14,24,34,44]
        ]

    return estrazioni

if __name__ == "__main__":
    dati = scarica()
    salva_storico(dati)













