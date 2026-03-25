import json
from statistics import mean

# ---------------------------
# CONFIG
# ---------------------------
WINDOW_BREVE = 25
WINDOW_LUNGO = 300

# ---------------------------
# CARICA ESTRAZIONI
# ---------------------------
with open("estrazioni.json") as f:
    estrazioni = json.load(f)

# ---------------------------
# FUNZIONI
# ---------------------------

def trova_posizioni(estrazioni, numero):
    pos = []
    for i, estr in enumerate(estrazioni):
        if numero in estr:
            pos.append(i)
    return pos

def ciclometria(estrazioni, numero):
    pos = trova_posizioni(estrazioni, numero)

    if len(pos) < 2:
        return 0

    cicli = []
    for i in range(1, len(pos)):
        cicli.append(pos[i] - pos[i-1])

    ciclo_medio = mean(cicli)
    ciclo_attuale = len(estrazioni) - pos[-1]

    if ciclo_medio == 0:
        return 0

    return round(ciclo_attuale / ciclo_medio, 2)

def frequenza(estrazioni, numero):
    count = sum(1 for estr in estrazioni if numero in estr)
    return count / len(estrazioni)

def indice(numero, estrazioni):
    freq = frequenza(estrazioni, numero)
    ciclo = ciclometria(estrazioni, numero)

    # indice combinato
    score = (freq * 10) + ciclo
    return round(score, 2)

def saturazione(estrazioni):
    totale = len(estrazioni)
    return round(len(estrazioni[-WINDOW_BREVE:]) / totale, 2)

# ---------------------------
# MAIN
# ---------------------------

risultati = {}

for ruota, estr_list in estrazioni.items():

    ultima = estr_list[-1]

    # numeri più frequenti
    conteggi = {}
    for estr in estr_list[-WINDOW_LUNGO:]:
        for n in estr:
            conteggi[n] = conteggi.get(n, 0) + 1

    # caldi = top 2
    caldi = sorted(conteggi, key=conteggi.get, reverse=True)[:2]

    # ambo
    ambo = caldi

    # ciclometria
    ciclo_vals = [ciclometria(estr_list, n) for n in ambo]

    # indice
    indice_vals = [indice(n, estr_list) for n in ambo]

    risultati[ruota] = {
        "ruota": ruota,
        "ultima": ultima,
        "caldi": caldi,
        "ambo": ambo,
        "ciclo": ciclo_vals,
        "indice": indice_vals,
        "saturazione": saturazione(estr_list)
    }

# ---------------------------
# SALVA
# ---------------------------

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)

print("✅ risultati.json aggiornato")