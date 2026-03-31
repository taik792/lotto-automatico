import json
from collections import Counter

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia"
]

def carica_estrazioni():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

def analizza_ruota(estrazioni_ruota):
    if not estrazioni_ruota or len(estrazioni_ruota) < 2:
        return {
            "ultima": [],
            "ambo": [0, 0],
            "score": 0
        }

    # ultime 5 estrazioni (dal più recente)
    ultime_estrazioni = estrazioni_ruota[-5:]
    ultima = ultime_estrazioni[-1]

    # frequenze ultime 20 estrazioni
    storico = estrazioni_ruota[-20