import json
from collections import Counter
from itertools import combinations

ordine_ruote = [
"Bari","Cagliari","Firenze","Genova","Milano",
"Napoli","Palermo","Roma","Torino","Venezia"
]

with open("estrazioni.json") as f:
    estrazioni = json.load(f)

risultati = []
giocate = []

for ruota in ordine_ruote:

    dati = estrazioni[ruota]

    ultima = dati[-1]

    ultime30 = dati[-30:]

    # frequenze numeri
    freq = Counter()

    for estr in ultime30:
        for n in estr:
            freq[n] += 1

    ordinati = sorted(freq.items(), key=lambda x: x[1], reverse=True)

    numeri_caldi = [ordinati[0][0], ordinati[1][0]]

    # ciclometria
    a = ultima[0]
    b = ultima[1]

    d = abs(a-b)
    c = 90-d

    ciclometria = [
        f"{a}-{b}",
        f"{d}-{c}"
    ]

    saturazione = round(sum(freq.values())/len(freq),2)

    # candidato 1 numeri caldi
    ambo1 = f"{numeri_caldi[0]}-{numeri_caldi[1]}"
    score1 = freq[numeri_caldi[0]] + freq[numeri_caldi[1]] + saturazione

    # candidato 2 ciclometria
    ambo2 = f"{d}-{c}"
    score2 = freq.get(d,0) + freq.get(c,0) + saturazione

    # bonus ciclometria
    bonus = 0

    if numeri_caldi[0] in [a,b,d,c]:
        bonus += 3

    if numeri_caldi[1] in [a,b,d,c]:
        bonus += 3

    score1 += bonus

    # candidato 3 ambo storico
    coppie = Counter()

    for estr in ultime30:
        for x,y in combinations(sorted(estr),2):
            coppie[(x,y)] += 1

    ambo_storico = max(coppie, key=coppie.get)

    ambo3 = f"{ambo_storico[0]}-{ambo_storico[1]}"
    score3 = coppie[ambo_storico] * 2 + saturazione

    # scelta intelligente
    candidati = [
        (ambo1,score1),
        (ambo2,score2),
        (ambo3,score3)
    ]

    candidati = sorted(candidati, key=lambda x: x[1], reverse=True)

    migliore = candidati[0]
    secondo = candidati[1]

    if migliore[1] - secondo[1] <= 2:
        ambo_forte = secondo[0]
        score = secondo[1]
    else:
        ambo_forte = migliore[0]
        score = migliore[1]

    giocate.append({
        "ruota":ruota,
        "ambo":ambo_forte,
        "score":score
    })

    risultati.append({
        "ruota":ruota,
        "ultima":ultima,
        "numeri_caldi":numeri_caldi,
        "ambo_forte":ambo_forte,
        "ciclometria":ciclometria,
        "saturazione":saturazione
    })

# migliori giocate del giorno
giocate_top = sorted(giocate, key=lambda x: x["score"], reverse=True)[:3]

output = {
    "ruote":risultati,
    "giocate_top":giocate_top
}

with open("risultati.json","w") as f:
    json.dump(output,f,indent=4)