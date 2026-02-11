import requests
import json
import csv
from io import StringIO

URL = "https://www.superenalotto.it/sites/default/files/archivio-estrazioni-lotto.csv"
FILE = "storico.json"

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def salva_storico(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def scarica():
    r = requests.get(URL, timeout=20)
    r.raise_for_status()

    csv_data = StringIO(r.text)
    reader = csv.DictReader(csv_data)

    estrazioni = {r: [] for r in RUOTE}

    # prendiamo l'ultima estrazione disponibile
    rows = list(reader)
    ultima = rows[-1]

    for ruota in RUOTE:
        numeri = []
        for i in range(1, 6):
            colonna = f"{ruota}_{i}"
            if colonna in ultima:
                try:
                    numeri.append(int(ultima[colonna]))
                except:
                    pass
        estrazioni[ruota] = numeri

    return estrazioni

if __name__ == "__main__":
    dati = scarica()
    salva_storico(dati)









