import json
from itertools import combinations

with open("estrazioni.json") as f:
    estrazioni = json.load(f)

print("\nANALISI AMBI STORICI\n")

for ruota in estrazioni:

    dati = estrazioni[ruota]

    conteggio = {}

    for estrazione in dati:

        ambi = list(combinations(estrazione,2))

        for a in ambi:

            a = tuple(sorted(a))

            conteggio[a] = conteggio.get(a,0)+1


    top = sorted(conteggio.items(), key=lambda x:x[1], reverse=True)[:10]

    print("\nRUOTA:", ruota)

    for ambo, n in top:

        print(ambo,"uscito",n,"volte")