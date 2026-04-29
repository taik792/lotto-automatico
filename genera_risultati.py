import json
from itertools import combinations

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia","Nazionale"]

# ===== CARICA DATI =====
with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {
    "top": [],
    "ruote": {},
    "giocate": [],
    "jolly": {}
}

# ===== FREQUENZE =====
def calcola_freq(lista):
    freq = {}
    for estr in lista:
        for n in estr:
            freq[n] = freq.get(n, 0) + 1
    return freq

# ===== CO-OCCORRENZA =====
def calcola_cooccorrenze(lista):
    coppie = {}
    for estr in lista:
        for a, b in combinations(sorted(estr), 2):
            coppie[(a, b)] = coppie.get((a, b), 0) + 1
    return coppie

# ===== ANALISI RUOTE =====
for ruota in RUOTE:

    if ruota not in estrazioni:
        continue

    estrazioni_ruota = estrazioni[ruota]

    if len(estrazioni_ruota) < 50:
        continue

    ultime = estrazioni_ruota[-1]

    breve = estrazioni_ruota[-20:]
    medio = estrazioni_ruota[-2000:]
    lungo = estrazioni_ruota[-3000:]

    freq_breve = calcola_freq(breve)
    freq_medio = calcola_freq(medio)
    freq_lungo = calcola_freq(lungo)

    cooc = calcola_cooccorrenze(medio)

    # ===== RITARDI =====
    ritardi = {}
    for n in range(1, 91):
        ritardo = 0
        for estr in reversed(estrazioni_ruota):
            if n in estr:
                break
            ritardo += 1
        ritardi[n] = ritardo

    # ===== SCORE NUMERI =====
    score_num = {}
    ultime_5 = estrazioni_ruota[-5:]

    for n in range(1, 91):

        penalita = 10 if n in ultime else 0
        presenze_recenti = sum(1 for estr in ultime_5 if n in estr)
        bonus_vicini = 1 if (n-1 in ultime or n+1 in ultime) else 0

        score = (
            freq_breve.get(n, 0) * 3 +
            freq_medio.get(n, 0) * 1.5 +
            freq_lungo.get(n, 0) * 1 +
            (ritardi[n] ** 1.15) * 0.6 +
            presenze_recenti * 2 +
            bonus_vicini -
            penalita
        )

        if ritardi[n] > 20:
            score += ritardi[n] * 0.25

        if freq_breve.get(n, 0) > 2 and freq_lungo.get(n, 0) > 15:
            score += 5

        score_num[n] = score

    # ===== SCELTA AMBO INTELLIGENTE =====

    candidati = [n for n in range(1, 91) if n not in ultime]

    # dividi numeri
    ritardatari = [n for n in candidati if ritardi[n] > 20]
    frequenti = [n for n in candidati if freq_breve.get(n, 0) >= 2]

    top_numeri = sorted(candidati, key=lambda x: score_num[x], reverse=True)[:20]

    miglior_ambo = None
    miglior_score = 0

    # ===== 1. MIX FORZATO =====
    for a in ritardatari:
        for b in frequenti:

            if a == b:
                continue

            base = score_num[a] + score_num[b]
            coppia = tuple(sorted((a, b)))
            co_score = cooc.get(coppia, 0)

            score_finale = base + (co_score * 4)

            if score_finale > miglior_score:
                miglior_score = score_finale
                miglior_ambo = [a, b]

    # ===== 2. FALLBACK =====
    if not miglior_ambo:
        for a, b in combinations(top_numeri, 2):

            penalty = 1
            if ritardi[a] > 25 and ritardi[b] > 25:
                penalty = 0.6

            base = score_num[a] + score_num[b]
            coppia = tuple(sorted((a, b)))
            co_score = cooc.get(coppia, 0)

            score_finale = (base + co_score * 4) * penalty

            if score_finale > miglior_score:
                miglior_score = score_finale
                miglior_ambo = [a, b]

    risultati["ruote"][ruota] = {
        "ultima": ultime,
        "ambo": miglior_ambo,
        "score": round(miglior_score, 2)
    }

# ===== TOP 3 =====
top_sorted = sorted(
    risultati["ruote"].items(),
    key=lambda x: x[1]["score"],
    reverse=True
)

top3 = top_sorted[:3]

risultati["top"] = [t[0] for t in top3]

giocate = []
for ruota, dati in top3:
    giocate.append({
        "ruota": ruota,
        "ambo": dati["ambo"]
    })

risultati["giocate"] = giocate

# ===== JOLLY =====

gemelle = {
    "Bari": "Napoli",
    "Napoli": "Bari",
    "Milano": "Torino",
    "Torino": "Milano",
    "Palermo": "Cagliari",
    "Cagliari": "Palermo",
    "Firenze": "Genova",
    "Genova": "Firenze"
}

miglior_ambo = None
miglior_score = 0
ruota_origine = None

for ruota, dati in risultati["ruote"].items():
    if dati["score"] > miglior_score:
        miglior_score = dati["score"]
        miglior_ambo = dati["ambo"]
        ruota_origine = ruota

ruote_top = [g["ruota"] for g in risultati["giocate"]]

ruota_jolly = gemelle.get(ruota_origine)

if ruota_jolly not in risultati["ruote"] or ruota_jolly in ruote_top:
    candidati = [
        r for r in risultati["ruote"]
        if r != ruota_origine and r not in ruote_top
    ]
    if candidati:
        ruota_jolly = max(candidati, key=lambda r: risultati["ruote"][r]["score"])
    else:
        ruota_jolly = ruota_origine

risultati["jolly"] = {
    "ruota": ruota_jolly,
    "ambo": miglior_ambo
}

# ===== SALVA =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2)

print("🔥 MOTORE PRO V2 ATTIVO (AMBI REALI + MIX INTELLIGENTE)")
