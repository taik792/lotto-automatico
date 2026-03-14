import json
from itertools import combinations
from collections import Counter

# carica estrazioni
with open("estrazioni.json") as f:
    estrazioni = json.load(f)

print("\n🔥 AMBO ENGINE LOTTO EVOLUTION\n")

for ruota in estrazioni:

    dati = estrazioni[ruota]

    ultime200 = dati[-200:]
    ultime50 = dati[-50:]

    # ----------------
    # numeri caldi
    # ----------------
    freq = Counter()

    for estrazione in ultime50:
        for numero in estrazione:
            freq[numero] += 1

    numeri_caldi = [n for n,_ in freq.most_common(10)]

    # ----------------
    # ambi recenti
    # ----------------
    ambi = Counter()

    for estrazione in ultime200:
        for ambo in combinations(estrazione,2):
            ambi[tuple(sorted(ambo))] += 1

    # ----------------
    # punteggio ambo
    # ----------------
    score_ambi = []

    for ambo, freq_ambo in ambi.items():

        score = freq_ambo

        # bonus numeri caldi
        if ambo[0] in numeri_caldi:
            score += 2

        if ambo[1] in numeri_caldi:
            score += 2

        score_ambi.append((ambo,score))

    # ----------------
    # migliori ambi
    # ----------------
    top = sorted(score_ambi,key=lambda x:x[1],reverse=True)[:5]

    print("\nRUOTA:",ruota)

    for ambo,score in top:
        print("AMBO:",ambo,"SCORE:",score)