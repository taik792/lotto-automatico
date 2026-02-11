import requests
import json
from bs4 import BeautifulSoup

URL = "https://www.lottomatica.it/lotto/ultime-estrazioni"
FILE = "storico.json"
MAX_ESTRAZIONI = 5

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
    r = requests.get(URL, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")
    estrazioni = {}

    for tab in soup.find_all("table"):
        for row in tab.find_all("tr"):
            celle = row.find_all("td")
            if len(celle) >= 6:
                ruota = celle[0].get_text(strip=True)
                if ruota in RUOTE:
                    numeri = [int(c.get_text()) for c in celle[1:6]]
                    estrazioni[ruota] = numeri
    return estrazioni

storico = leggi_storico()
nuove = scarica()

for ruota, numeri in nuove.items():
    if numeri not in storico[ruota]:
        storico[ruota].insert(0, numeri)
        storico[ruota] = storico[ruota][:MAX_ESTRAZIONI]

salva_storico(storico)
print("Aggiornamento completato")
