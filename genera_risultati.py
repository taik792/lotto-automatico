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

    ultime_estrazioni = estrazioni_ruota[-5:]
    ultima = ultime_estrazioni[-1]

    storico = estrazioni_ruota[-20:]
    numeri = [n for estr in storico for n in estr]

    freq = Counter(numeri)
    numeri_ordinati = [n for n, _ in freq.most_common()]

    candidati = [n for n in numeri_ordinati if n not in ultima]

    if len(candidati) < 2:
        candidati = numeri_ordinati

    if len(candidati) < 2:
        candidati = list(range(1, 91))

    ambo = candidati[:2]

    score = freq[ambo[0]] + freq[ambo[1]]

    return {
        "ultima": ultima,
        "ambo": ambo,
        "score": score
    }

def genera():
    dati = carica_estrazioni()
    risultati = {}

    for ruota in RUOTE:
        estrazioni_ruota = dati.get(ruota, [])
        risultati[ruota] = analizza_ruota(estrazioni_ruota)

    top = sorted(risultati.items(), key=lambda x: x[1]["score"], reverse=True)[:5]

    output = {
        "top": [r[0] for r in top],
        "ruote": risultati
    }

    with open("risultati.json", "w") as f:
        json.dump(output, f, indent=2)

    print("OK generato")

if __name__ == "__main__":
    genera()