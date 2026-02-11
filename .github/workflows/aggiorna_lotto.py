import requests
import json
from bs4 import BeautifulSoup

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
    r = requests.get(URL, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    estrazioni = {r: [] for r in RUOTE}

    tabelle = soup.find_all("table")

    for tabella in tabelle:
        righe = tabella.find_all("tr")
        for riga in righe:
            celle = riga.find_all("td")
            if len(celle) >= 6:
                ruota = celle[0].get_text(strip=True)
                if ruota in RUOTE:
                    numeri = []
                    for c in celle[1:6]:
                        try:
                            numeri.append(int(c.get_text(strip=True)))
                        except:
                            pass
                    estrazioni[ruota] = numeri

    return estrazioni

if __name__ == "__main__":
    dati = scarica()
    salva_storico(dati)








