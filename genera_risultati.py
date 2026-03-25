import json

RUOTE = [
    "Bari","Cagliari","Firenze","Genova",
    "Milano","Napoli","Palermo","Roma",
    "Torino","Venezia"
]

# =========================
# CARICA DATI
# =========================
with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

risultati = {}

# =========================
# FUNZIONI
# =========================

def ritardo_numero(lista_estrazioni, numero):
    """
    Quante estrazioni sono passate dall’ultima uscita
    """
    for i, estr in enumerate(reversed(lista_estrazioni)):
        if numero in estr:
            return i
    return len(lista_estrazioni)


def numeri_caldi(lista, n=2):
    """
    Numeri più frequenti nelle ultime 25
    """
    freq = {}
    ultime = lista[-25:]

    for estr in ultime:
        for num in estr:
            freq[num] = freq.get(num, 0) + 1

    return sorted(freq, key=freq.get, reverse=True)[:n]


def calcola_saturazione(lista):
    """
    Saturazione = varietà numeri ultime 50 estrazioni
    """
    ultime = lista[-50:]
    tutti = []

    for estr in ultime:
        tutti.extend(estr)

    unici = len(set(tutti))
    return round(unici / 90, 2)


def calcola_indice(r1, r2):
    """
    Indice basato su ritardi (più alto = più interessante)
    """
    media = (r1 + r2) / 2
    diff = abs(r1 - r2)

    indice1 = round(media / 5, 2)
    indice2 = round(diff / 3, 2)

    return [indice1, indice2]


# =========================
# LOOP PRINCIPALE
# =========================

for ruota in RUOTE:

    estr = estrazioni.get(ruota, [])

    if not estr:
        continue

    ultima = estr[-1]

    caldi = numeri_caldi(estr)

    if len(caldi) < 2:
        continue

    n1, n2 = caldi

    # CICLOMETRIA REALE
    r1 = ritardo_numero(estr, n1)
    r2 = ritardo_numero(estr, n2)

    ciclo = [r1, r2]

    # INDICE
    indice = calcola_indice(r1, r2)

    # SATURAZIONE
    saturazione = calcola_saturazione(estr)

    risultati[ruota] = {
        "ruota": ruota,
        "ultima": ultima,
        "caldi": [n1, n2],
        "ambo": [n1, n2],
        "ciclo": ciclo,
        "indice": indice,
        "saturazione": saturazione
    }

# =========================
# SALVA FILE
# =========================

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)

print("✅ Risultati aggiornati")