import requests
import json

FILE = "storico.json"

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

URL = "https://api.npoint.io/5d3f7f7c5a1b4c2d9c4b"

def salva_storico(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def scarica():
    r = requests.get(URL, timeout=15)
    data = r.json()

    risultato = {r: [] for r in RUOTE}

    for ruota in RUOTE:
        if ruota in data:
            risultato[ruota] = data[ruota]

    return risultato

dati = scarica()
salva_storico(dati)

print("Aggiornamento completato")



