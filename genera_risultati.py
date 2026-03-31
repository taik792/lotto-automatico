import json

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia"]

with open("estrazioni.json") as f:
    estrazioni = json.load(f)

risultati = {"top": [], "ruote": {}}

for ruota in RUOTE:
    estrazioni_ruota = [e[ruota] for e in estrazioni if ruota in e]

    ultime = estrazioni_ruota[-1]
    storico = estrazioni_ruota[-20:]

    # frequenze
    freq = {}
    for estr in storico:
        for n in estr:
            freq[n] = freq.get(n, 0) + 1

    # ritardi
    ritardi = {}
    for n in range(1, 91):
        ritardo = 0
        for estr in reversed(estrazioni_ruota):
            if n in estr:
                break
            ritardo += 1
        ritardi[n] = ritardo

    # score combinato
    score_num = {}
    for n in freq:
        score_num[n] = freq[n] + (ritardi[n] / 2)

    # togli numeri usciti
    candidati = [n for n in score_num if n not in ultime]

    # ordina
    candidati.sort(key=lambda x: score_num[x], reverse=True)

    if len(candidati) >= 2:
        ambo = [candidati[0], candidati[1]]
        score = round(score_num[ambo[0]] + score_num[ambo[1]])
    else:
        ambo = []
        score = 0

    risultati["ruote"][ruota] = {
        "ultima": ultime,
        "ambo": ambo,
        "score": score
    }

# TOP 5 reali
top = sorted(risultati["ruote"].items(), key=lambda x: x[1]["score"], reverse=True)
risultati["top"] = [t[0] for t in top[:5]]

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)