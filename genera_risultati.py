import json
from collections import Counter

RUOTE = [
    "Bari","Cagliari","Firenze","Genova",
    "Milano","Napoli","Palermo","Roma",
    "Torino","Venezia"
]

ULTIME_ESTRAZIONI_ANALISI = 30  # puoi aumentare

def carica_estrazioni():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

def analizza_ruota(ruota, dati):
    if ruota not in dati or len(dati[ruota]) == 0:
        return {
            "ruota": ruota,
            "ambo": [1, 2],
            "score": 0
        }

    estrazioni = dati[ruota]

    # prendi ultime N estrazioni
    ultime = estrazioni[-ULTIME_ESTRAZIONI_ANALISI:]

    # numeri appena usciti (ultima estrazione)
    ultimi_usciti = set(estrazioni[-1])

    # conta frequenze
    freq = Counter()
    for estr in ultime:
        freq.update(estr)

    # ordina per frequenza
    numeri_ordinati = [n for n, _ in freq.most_common()]

    # filtra numeri appena usciti
    candidati = [n for n in numeri_ordinati if n not in ultimi_usciti]

    # fallback se troppo pochi
    if len(candidati) < 2:
        candidati = numeri_ordinati

    # scegli ambo
    ambo = candidati[:2]

    # score = somma frequenze + bonus ritardo
    score = freq[ambo[0]] + freq[ambo[1]]

    # piccolo bonus se non usciti recentemente
    bonus = 0
    for n in ambo:
        if n not in ultimi_usciti:
            bonus += 2

    score += bonus

    return {
        "ruota": ruota,
        "ambo": ambo,
        "score": round(score, 2)
    }

def genera():
    dati = carica_estrazioni()

    risultati = {}

    for ruota in RUOTE:
        risultati[ruota] = analizza_ruota(ruota, dati)

    # salva
    with open("risultati.json", "w") as f:
        json.dump(risultati, f, indent=2)

    print("✅ risultati.json generato correttamente")

if __name__ == "__main__":
    genera()