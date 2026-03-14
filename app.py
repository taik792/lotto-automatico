import json

# carica le estrazioni
with open("estrazioni.json", "r") as f:
    data = json.load(f)

risultati = []

# ordine ufficiale delle ruote
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

for ruota in ordine_ruote:

    if ruota not in data:
        continue

    estrazioni = data[ruota]

    if len(estrazioni) < 10:
        continue

    # ultima estrazione
    ultima = estrazioni[-1]

    # ultime 50 estrazioni
    storico = estrazioni[-50:]

    frequenza = {}

    for estrazione in storico:
        for numero in estrazione:

            if numero not in frequenza:
                frequenza[numero] = 0

            frequenza[numero] += 1

    # ordina per frequenza
    ordinati = sorted(frequenza.items(), key=lambda x: x[1], reverse=True)

    numeri_caldi = [
        ordinati[0][0],
        ordinati[1][0]
    ]

    ambo = f"{numeri_caldi[0]} - {numeri_caldi[1]}"

    saturazione = round(
        sum(frequenza.values()) / len(frequenza),
        2
    )

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