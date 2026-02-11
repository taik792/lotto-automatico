import requests
import json
from bs4 import BeautifulSoup

URL = "https://www.superenalotto.it/estrazioni/lotto"
FILE = "storico.json"

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def scarica():
    r = requests.get(URL, timeout=15)
    soup = BeautifulSoup(r.text, "html.parser")

    estrazioni = {r: [] for r in RUOTE}

    for tab in soup.find_all("table"):
        for row in tab.find_all("tr"):
            celle = row.find_all("td")
            if len(celle) >= 6:
                ruota = celle[0].get_text(strip=True)
                if ruota in RUOTE:
                    numeri = []
                    for c in celle[1:6]:
                        testo = c.get_text(strip=True)
                        if testo.isdigit():
                            numeri.append(int(testo))
                    if len(numeri) == 5:
                        estrazioni[ruota] = numeri

    return estrazioni


def salva_storico(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    dati = scarica()
    salva_storico(dati)

