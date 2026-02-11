import requests
import json

URL = "https://www.superenalotto.it/sites/default/files/archivio-lotto/estrazioni-lotto.csv"
FILE = "storico.json"
MAX_ESTRAZIONI = 5

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def salva_storico(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def scarica():
    r = requests.get(URL)
    righe = r.text.splitlines()
    
    estrazioni = {ruota: [] for ruota in RUOTE}

    # saltiamo intestazione
    for riga in righe[1:]:
        parti = riga.split(";")
        if len(parti) < 12:
            continue

        ruota = parti[1]
        numeri = list(map(int, parti[2:7]))

        if ruota in RUOTE:
            if len(estrazioni[ruota]) < MAX_ESTRAZIONI:
                estrazioni[ruota].append(numeri)

    return estrazioni

if __name__ == "__main__":
    dati = scarica()
    salva_storico(dati)

