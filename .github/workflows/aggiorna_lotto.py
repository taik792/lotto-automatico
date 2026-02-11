import json
import requests

URL = "https://api.allorigins.win/raw?url=https://www.superenalotto.it/estrazioni/lotto"
FILE = "storico.json"

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def salva(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def genera_dati_test():
    return {
        "Bari": [11,22,33,44,55],
        "Cagliari": [1,2,3,4,5],
        "Firenze": [6,7,8,9,10],
        "Genova": [10,20,30,40,50],
        "Milano": [5,15,25,35,45],
        "Napoli": [9,19,29,39,49],
        "Palermo": [7,17,27,37,47],
        "Roma": [8,18,28,38,48],
        "Torino": [12,24,36,48,60],
        "Venezia": [13,23,33,43,53],
        "Nazionale": [90,80,70,60,50]
    }

if __name__ == "__main__":
    dati = genera_dati_test()
    salva(dati)










