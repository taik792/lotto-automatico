import requests
import json

URL = "https://api.superenalotto.it/estrazioni/lotto/latest"
FILE = "storico.json"

def salva_storico(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)

def scarica():
    try:
        r = requests.get(URL, timeout=10)
        dati = r.json()
        return dati
    except:
        return {}

if __name__ == "__main__":
    dati = scarica()
    salva_storico(dati)







