import json
from collections import Counter

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia"
]

def carica():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

def analizza(estrazioni):
    if not estrazioni:
        return {"ultima": [], "ambo": [0,0], "score": 0}

    ultima = estrazioni[-1]
    storico = estrazioni[-20:]

    numeri = [n for estr in storico for n in estr]
    freq = Counter(numeri)

    ordinati = [n for n,_ in freq.most_common()]
    candidati = [n for n in ordinati if n not in ultima]

    if len(candidati) < 2:
        candidati = ordinati

    if len(candidati) < 2:
        candidati = list(range(1,91))

    ambo = candidati[:2]
    score = freq.get(ambo[0],0) + freq.get(ambo[1],0)

    return {
        "ultima": ultima,
        "ambo": ambo,
        "score": score
    }

def main():
    dati = carica()
    risultati = {}

    for r in RUOTE:
        risultati[r] = analizza(dati.get(r, []))

    top = sorted(risultati.items(), key=lambda x: x[1]["score"], reverse=True)[:5]

    output = {
        "top": [t[0] for t in top],
        "ruote": risultati
    }

    with open("risultati.json", "w") as f:
        json.dump(output, f, indent=2)

    print("OK")

if __name__ == "__main__":
    main()