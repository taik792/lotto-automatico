import requests
import json

FILE = "storico.json"
MAX_ESTRAZIONI = 5

URL = "https://www.superenalotto.it/estrazioni/lotto"

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def leggi_storico():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return {r: [] for r in RUOTE}

def salva_storico(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def scarica():
    r = requests.get(URL, timeout=20)
    testo = r.text

    dati = {r: [] for r in RUOTE}

    for ruota in RUOTE:
        start = testo.find(ruota)
        if start != -1:
            parte = testo[start:start+300]
            numeri = []
            for token in parte.split():
                if token.isdigit():
                    numeri.append(int(token))
            if len(numeri) >= 5:
                dati[ruota] = numeri[:5]

    return dati

dati = scarica()
salva_storico(dati)
print("Aggiornamento completato")

