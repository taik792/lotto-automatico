import requests
import json

FILE = "storico.json"
MAX_ESTRAZIONI = 5

URL = "https://www.superenalotto.it/rest/estrazioni/lotto"

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def salva_storico(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def scarica():
    r = requests.get(URL)
    data = r.json()

    risultato = {r: [] for r in RUOTE}

    for estrazione in data[:MAX_ESTRAZIONI]:
        for ruota in RUOTE:
            numeri = estrazione["ruote"].get(ruota)
            if numeri:
                risultato[ruota] = numeri

    return risultato

dati = scarica()
salva_storico(dati)
print("Aggiornamento completato")


