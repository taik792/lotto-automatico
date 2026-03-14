import json
from collections import Counter
from itertools import combinations

ordine_ruote = [
"Bari",
"Cagliari",
"Firenze",
"Genova",
"Milano",
"Napoli",
"Palermo",
"Roma",
"Torino",
"Venezia"
]

with open("estrazioni.json") as f:
    estrazioni = json.load(f)

risultati = []

for ruota in ordine_ruote:

    dati = estrazioni[ruota]

    ultima = dati[-1]

    ultime_estrazioni = dati[-30:]
    ultime_ambo = dati[-200:]

    # -------------------------
    # NUMERI CALDI
    # -------------------------

    freq = Counter()

    for estr in ultime_estrazioni:
        for n in estr:
            freq[n] += 1

    numeri_caldi = [n for n,_ in freq.most_common(2)]

    # -------------------------
    # AMBO STATISTICO
    # -------------------------

    ambi = Counter()

    for estr in ultime_ambo:
        for a,b in combinations(estr,2):
            ambi[tuple(sorted((a,b)))] += 1

    ambo_top = ambi.most_common(1)[0][0]
    ambo_forte = f"{ambo_top[0]}-{ambo_top[1]}"

    # -------------------------
    # CICLOMETRIA
    # -------------------------

    a = ultima[0]
    b = ultima[1]

    d = abs(a-b)
    d2 = 90-d

    c1 = (b+d) % 90
    c2 = (b+d2) % 90

    if c1 == 0:
        c1 = 90

    if c2 == 0:
        c2 = 90

    ciclometria = [
        f"{a}-{b}",
        f"{b}-{c1}",
        f"{b}-{c2}"
    ]

    # -------------------------
    # SATURAZIONE
    # -------------------------

    saturazione = round(sum(freq.values())/len(freq),2)

    risultati.append({

        "ruota":ruota,
        "ultima":ultima,
        "numeri_caldi":numeri_caldi,
        "ambo_forte":ambo_forte,
        "ciclometria":ciclometria,
        "saturazione":saturazione

    })

output = {
"ruote": risultati
}

with open("risultati.json","w") as f:
    json.dump(output,f,indent=4)