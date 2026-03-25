import json

RUOTE = [
    "Bari","Cagliari","Firenze","Genova",
    "Milano","Napoli","Palermo","Roma",
    "Torino","Venezia"
]

with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

risultati = {}

def ritardo_numero(lista, numero):
    for i, estr in enumerate(reversed(lista)):
        if numero in estr:
            return i
    return len(lista)


def trova_ritardatari(lista):
    ritardi = {}

    for n in range(1, 91):
        ritardi[n] = ritardo_numero(lista, n)

    ordinati = sorted(ritardi, key=ritardi.get, reverse=True)

    return ordinati[:2], ritardi


def calcola_saturazione(lista):
    ultime = lista[-50:]
    numeri = []

    for estr in ultime:
        numeri += estr

    return round(len(set(numeri)) / 90, 2)


for ruota in RUOTE:

    estr = estrazioni.get(ruota, [])

    if not estr:
        continue

    ultima = estr[-1]

    # 🔥 NUMERI RITARDATARI (NON CALDI)
    ambo, mappa = trova_ritardatari(estr)

    n1, n2 = ambo

    ciclo = [mappa[n1], mappa[n2]]

    indice = [
        round(ciclo[0] / 5, 2),
        round(ciclo[1] / 5, 2)
    ]

    saturazione = calcola_saturazione(estr)

    risultati[ruota] = {
        "ruota": ruota,
        "ultima": ultima,
        "caldi": ambo,
        "ambo": ambo,
        "ciclo": ciclo,
        "indice": indice,
        "saturazione": saturazione
    }

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)

print("✅ CICLOMETRIA REALE ATTIVA")