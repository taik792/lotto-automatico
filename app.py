import json
from itertools import combinations
from collections import Counter

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

# coppie ruote ciclometriche
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

for ruota in ordine_ruote:

    dati = estrazioni[ruota]

    ultima = dati[-1]

    ultime = dati[-30:]

    freq = {}

    for estr in ultime:
        for n in estr:
            freq[n] = freq.get(n,0)+1

    ordinati = sorted(freq.items(), key=lambda x:x[1], reverse=True)

    numeri_caldi = [ordinati[0][0], ordinati[1][0]]

    ambo_forte = f"{numeri_caldi[0]}-{numeri_caldi[1]}"

    saturazione = round(sum(freq.values())/len(freq),2)

    # ------------------------
    # CICLOMETRIA RUOTA
    # ------------------------

    a = ultima[0]
    b = ultima[1]

    d = abs(a-b)

    d2 = 90-d

    c1 = (b+d)%90
    c2 = (b+d2)%90

    if c1 == 0:
        c1 = 90

    if c2 == 0:
        c2 = 90

    ciclometria_ruota = [
        f"{a}-{b}",
        f"{b}-{c1}",
        f"{b}-{c2}"
    ]

    # ------------------------
    # AMBI STATISTICI
    # ------------------------

    ultime200 = dati[-200:]

    conta_ambi = Counter()

    for estr in ultime200:
        for ambo in combinations(estr,2):
            conta_ambi[tuple(sorted(ambo))] += 1

    top_ambi = []

    for (x,y),freq_ambo in conta_ambi.most_common(5):
        top_ambi.append(f"{x}-{y}")

    risultati.append({
        "ruota":ruota,
        "ultima":ultima,
        "numeri_caldi":numeri_caldi,
        "ambo_forte":ambo_forte,
        "ambi_statistici":top_ambi,
        "ciclometria":ciclometria_ruota,
        "saturazione":saturazione
    })

# ------------------------
# CICLOMETRIA TRA RUOTE
# ------------------------

ciclometria_tra_ruote = []

for r1,r2 in coppie_ruote:

    e1 = estrazioni[r1][-1]
    e2 = estrazioni[r2][-1]

    for a,b in zip(e1,e2):

        d = abs(a-b)
        c = 90-d

        ciclometria_tra_ruote.append({
            "ruote":f"{r1}-{r2}",
            "ambo":f"{a}-{b}"
        })

        ciclometria_tra_ruote.append({
            "ruote":f"{r1}-{r2}",
            "ambo":f"{d}-{c}"
        })

output = {
    "ruote":risultati,
    "ciclometria_ruote":ciclometria_tra_ruote
}

with open("risultati.json","w") as f:
    json.dump(output,f,indent=4)