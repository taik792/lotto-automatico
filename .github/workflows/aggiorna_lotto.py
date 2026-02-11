import requests
import json

FILE = "storico.json"

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def salva_storico(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def scarica():
    url = "https://www.superenalotto.it/estrazioni/lotto"
    r = requests.get(url)
    testo = r.text

    dati = {r: [] for r in RUOTE}

    for ruota in RUOTE:
        if ruota in testo:
            dati[ruota] = [1,2,3,4,5]  # temporaneo per test

    return dati

dati = scarica()
salva_storico(dati)
print("Aggiornato!")





