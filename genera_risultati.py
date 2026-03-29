import json
from statistics import mean
from ambo_engine import genera_giocata_top

# ---------------------------
# CONFIG
# ---------------------------
WINDOW_CICLO = 60
WINDOW_FREQ = 30
WINDOW_RECENTE = 10

# ---------------------------
# CARICA DATI
# ---------------------------
with open("estrazioni.json") as f:
    estrazioni = json.load(f)

# ---------------------------
# FUNZIONI
# ---------------------------

def ciclometria(estrazioni, numero):
    estr = estrazioni[-WINDOW_CICLO:]

    pos = []
    for i, e in enumerate(estr):
        if numero in e:
            pos.append(i)

    if len(pos) < 2:
        return 0

    cicli = []
    for i in range(1, len(pos)):
        cicli.append(pos[i] - pos[i-1])

    ciclo_medio = mean(cicli)
    ciclo_attuale = len(estr) - pos[-1]

    if ciclo_medio == 0:
        return 0

    return round(ciclo_attuale / ciclo_medio, 2)


def frequenza(estrazioni, numero):
    estr = estrazioni[-WINDOW_FREQ:]
    count = sum(1 for e in estr if numero in e)
    return count / len(estr)


def recente(estrazioni, numero):
    estr = estrazioni[-WINDOW_RECENTE:]
    return sum(1 for e in estr if numero in e)


def indice(numero, estrazioni):
    f = frequenza(estrazioni, numero)
    c = ciclometria(estrazioni, numero)
    r = recente(estrazioni, numero)

    score = (c * 1.5) + (f * 10) + (r * 0.5)
    return round(score, 2)


def saturazione(estrazioni):
    ultimi = estrazioni[-30:]

    numeri = set()
    for estr in ultimi:
        numeri.update(estr)

    return round(len(numeri) / 90, 2)


# ---------------------------
# MAIN
# ---------------------------

risultati = {}

for ruota, estr_list in estrazioni.items():

    ultima = estr_list[-1]

    conteggi = {}
    for estr in estr_list[-WINDOW_FREQ:]:
        for n in estr:
            conteggi[n] = conteggi.get(n, 0) + 1

    caldi = sorted(conteggi, key=conteggi.get, reverse=True)[:2]
    ambo = caldi

    ciclo_vals = [ciclometria(estr_list, n) for n in ambo]
    indice_vals = [indice(n, estr_list) for n in ambo]

    risultati[ruota] = {
        "ruota": ruota,
        "ultima": ultima,
        "caldi": caldi,
        "ambo": ambo,
        "ambo_forte": ambo,  # per il motore
        "ciclo": ciclo_vals,
        "indice": indice_vals,
        "saturazione": saturazione(estr_list)
    }

# =========================
# 🔥 NUOVO MOTORE TOP PICK
# =========================

ruote_list = list(risultati.values())

top_pick = genera_giocata_top(ruote_list)

# =========================
# SALVATAGGIO COMPATIBILE SITO
# =========================

# aggiungiamo top_pick senza rompere il sito
risultati["top_pick"] = top_pick

with open("risultati.json", "w") as f:
    json.dump(risultati, f, indent=2)

# =========================
# DEBUG
# =========================

print("🔥 NUOVO MOTORE ATTIVO 🔥")
print("TOP PICK:")
for t in top_pick:
    print(t)