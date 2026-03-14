import json

# ordine ruote lotto
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

    # ultima estrazione
    ultima = dati[-1]

    # ultime 30 estrazioni
    ultime_estrazioni = dati[-30:]

    frequenze = {}

    for estr in ultime_estrazioni:
        for numero in estr:
            frequenze[numero] = frequenze.get(numero, 0) + 1

    # ordina frequenze
    ordinati = sorted(frequenze.items(), key=lambda x: x[1], reverse=True)

    numeri_caldi = [ordinati[0][0], ordinati[1][0]]

    ambo_forte = f"{numeri_caldi[0]} - {numeri_caldi[1]}"

    saturazione = round(sum(frequenze.values()) / len(frequenze), 2)

    # --------------------
    # CICLOMETRIA
    # --------------------

    a = ultima[0]
    b = ultima[1]

    distanza = abs(b - a)

    c1 = (b + distanza) % 90
    c2 = (c1 + distanza) % 90

    if c1 == 0:
        c1 = 90
    if c2 == 0:
        c2 = 90

    ambi_ciclometrici = [
        f"{a}-{b}",
        f"{b}-{c1}",
        f"{c1}-{c2}"
    ]

    risultati.append({
        "ruota": ruota,
        "ultima": ultima,
        "numeri_caldi": numeri_caldi,
        "ambo_forte": ambo_forte,
        "saturazione": saturazione,
        "ciclometria": ambi_ciclometrici
    })

# salva risultati
with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=4)