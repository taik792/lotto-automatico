import json
import random

# carica estrazioni
with open("estrazioni.json", "r") as f:
    data = json.load(f)

risultati = []

for ruota, estrazioni in data.items():

    if len(estrazioni) < 10:
        continue

    # ultima estrazione (LA PIÙ NUOVA)
    ultima = estrazioni[-1]

    # prendiamo le ultime 50 estrazioni
    storico = estrazioni[-50:]

    frequenza = {}

    for estrazione in storico:
        for numero in estrazione:

            if numero not in frequenza:
                frequenza[numero] = 0

            frequenza[numero] += 1

    # ordina per frequenza
    ordinati = sorted(frequenza.items(), key=lambda x: x[1], reverse=True)

    # numeri più frequenti
    numeri_caldi = [ordinati[0][0], ordinati[1][0]]

    # ambo forte
    ambo = f"{numeri_caldi[0]} - {numeri_caldi[1]}"

    # saturazione ruota
    saturazione = round(sum(frequenza.values()) / len(frequenza), 2)

    risultati.append({
        "ruota": ruota,
        "ultima": ultima,
        "numeri_caldi": numeri_caldi,
        "ambo_forte": ambo,
        "saturazione": saturazione
    })

# salva risultati
with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=4)