import requests
import json
import re

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
        pattern = ruota + r".*?(\d{1,2}).*?(\d{1,2}).*?(\d{1,2}).*?(\d{1,2}).*?(\d{1,2})"
        match = re.search(pattern, text, re.DOTALL)

        if match:
            numeri = [int(n) for n in match.groups()]
            estrazioni[ruota] = numeri

    return estrazioni

if __name__ == "__main__":
    dati = scarica()
    salva_storico(dati)






