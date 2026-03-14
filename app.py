import json

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

# carica estrazioni
with open("estrazioni.json") as f:
    estrazioni = json.load(f)

risultati = []

for ruota in ordine_ruote:

    dati = estrazioni[ruota]

    # prende ultima estrazione
    ultima = dati[-1]

    # prende ultime 10 estrazioni
    ultime_estrazioni = dati[-10:]

    frequenze = {}

    for estr in ultime_estrazioni:
        for numero in estr:
            frequenze[numero] = frequenze.get(numero, 0) + 1

    # ordina per frequenza
    ordinati = sorted(frequenze.items(), key=lambda x: x[1], reverse=True)

    numeri_caldi = [ordinati[0][0], ordinati[1][0]]

    ambo_forte = f"{numeri_caldi[0]} - {numeri_caldi[1]}"

    saturazione = round(sum(frequenze.values()) / len(frequenze), 2)

    risultati.append({
        "ruota": ruota,
        "ultima": ultima,
        "numeri_caldi": numeri_caldi,
        "ambo_forte": ambo_forte,
        "saturazione": saturazione
    })

# salva risultati per il sito
with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=4)