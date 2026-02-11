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
    r = requests.get(URL)
    text = r.text

    estrazioni = {r: [] for r in RUOTE}

    for ruota in RUOTE:
        if ruota in text:
            estrazioni[ruota] = [1,2,3,4,5]  # TEST

    return estrazioni

if __name__ == "__main__":
    dati = scarica()
    salva_storico(dati)






