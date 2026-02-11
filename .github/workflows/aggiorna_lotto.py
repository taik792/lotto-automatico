import requests
import json
import csv
from io import StringIO

FILE = "storico.json"
MAX_ESTRAZIONI = 5

CSV_URL = "https://raw.githubusercontent.com/matteocontrini/lotto-data/master/lotto.csv"

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def salva(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def scarica():
    r = requests.get(CSV_URL, timeout=20)
    r.raise_for_status()

    csv_data = csv.DictReader(StringIO(r.text))
    righe = list(csv_data)[-MAX_ESTRAZIONI:]

    risultato = {r: [] for r in RUOTE}

    for riga in righe:
        for ruota in RUOTE:
            key = ruota.lower()
            if key in riga and riga[key]:
                numeri = [int(n) for n in riga[key].split()]
                risultato[ruota] = numeri

    return risultato

dati = scarica()
salva(dati)

print("Aggiornamento completato")




