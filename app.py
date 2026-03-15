import json
from collections import Counter

ordine_ruote = [
"Bari","Cagliari","Firenze","Genova","Milano",
"Napoli","Palermo","Roma","Torino","Venezia"
]

coppie_ruote = [
("Bari","Napoli"),
("Cagliari","Palermo"),
("Firenze","Roma"),
("Genova","Torino"),
("Milano","Venezia")
]

with open("estrazioni.json") as f:
    estrazioni = json.load(f)

risultati = []
giocate = []

for ruota in ordine_ruote:

    dati = estrazioni[ruota]

    ultima = dati[-1]

    ultime30 = dati[-30:]

    freq = Counter()

    for estr in ultime30:
        for n in estr:
            freq[n] += 1

    ordinati = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    numeri_caldi = [ordinati[0][0], ordinati[1][0]]

    # ciclometria ruota
    a = ultima[0]
    b = ultima[1]

    d = abs(a-b)
    c = 90-d

    ciclometria = [
        f"{a}-{b}",
        f"{d}-{c}"
    ]

    saturazione = round(sum(freq.values())/len(freq),2)

    ambo1 = f"{numeri_caldi[0]}-{numeri_caldi[1]}"
    ambo2 = f"{d}-{c}"

    score1 = freq[numeri_caldi[0]] + freq[numeri_caldi[1]] + saturazione
    score2 = freq.get(d,0) + freq.get(c,0) + saturazione

    # bonus ciclometria
    bonus = 0

    if numeri_caldi[0] in [a,b,d,c]:
        bonus += 3

    if numeri_caldi[1] in [a,b,d,c]:
        bonus += 3

    score1 += bonus

    if score2 > score1:
        ambo_forte = ambo2
        score = score2
    else:
        ambo_forte = ambo1
        score = score1

    giocate.append({
        "ruota": ruota,
        "ambo": ambo_forte,
        "score": score
    })

    risultati.append({
        "ruota":ruota,
        "ultima":ultima,
        "numeri_caldi":numeri_caldi,
        "ambo_forte":ambo_forte,
        "ciclometria":ciclometria,
        "saturazione":saturazione
    })

# migliori giocate
giocate_top = sorted(giocate, key=lambda x:x["score"], reverse=True)[:3]

# ciclometria tra ruote
ciclometria_tra_ruote = []

for r1,r2 in coppie_ruote:

    e1 = estrazioni[r1][-1]
    e2 = estrazioni[r2][-1]

    for a,b in zip(e1,e2):

        d = abs(a-b)
        c = 90-d

        if d != 0:
            ciclometria_tra_ruote.append({
                "ruote":f"{r1}-{r2}",
                "ambo":f"{d}-{c}"
            })

output = {
    "ruote": risultati,
    "giocate_top": giocate_top,
    "ciclometria_ruote": ciclometria_tra_ruote
}

with open("risultati.json","w") as f:
    json.dump(output,f,indent=4)