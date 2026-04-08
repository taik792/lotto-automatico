import json
import random

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia","Nazionale"]

# ===== PARAMETRI DINAMICI =====
BREVE = 20
MEDIO = 100
LUNGO = 500

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

# ===== ANALISI =====
for ruota in RUOTE:

    if ruota not in estrazioni:
        continue

    estrazioni_ruota = estrazioni[ruota]

    if len(estrazioni_ruota) < 10:
        continue

    ultime = estrazioni_ruota[-1]

    breve = estrazioni_ruota[-min(BREVE, len(estrazioni_ruota)):]
    medio = estrazioni_ruota[-min(MEDIO, len(estrazioni_ruota)):]
    lungo = estrazioni_ruota[-min(LUNGO, len(estrazioni_ruota)):]

    freq_breve = calcola_freq(breve)
    freq_medio = calcola_freq(medio)
    freq_lungo = calcola_freq(lungo)

    # ===== RITARDI =====
    ritardi = {}
    for n in range(1, 91):
        ritardo = 0
        for estr in reversed(estrazioni_ruota):
            if n in estr:
                break
            ritardo += 1
        ritardi[n] = ritardo

    score_num = {}

    for n in range(1, 91):

        penalita = 10 if n in ultime else 0
        freq_b = freq_breve.get(n, 0)
        freq_m = freq_medio.get(n, 0)
        freq_l = freq_lungo.get(n, 0)

        score = (
            freq_b * 3 +
            freq_m * 1.5 +
            freq_l * 1 +
            (ritardi[n] * 0.6) -
            penalita
        )

        # BONUS ritardatari forti
        if ritardi[n] > 20:
            score += ritardi[n] * 0.5

        # BONUS numeri vivi (usciti ma non troppo)
        if 1 <= freq_b <= 2:
            score += 2

        # MICRO RANDOM per variare
        score += random.uniform(0, 0.3)

        score_num[n] = score

    # ===== SCELTA AMBO =====
    candidati = [n for n in range(1, 91) if n not in ultime]
    candidati.sort(key=lambda x: score_num[x], reverse=True)

    ambo = [candidati[0], candidati[1]]
    score_ambo = score_num[ambo[0]] + score_num[ambo[1]]

    risultati["ruote"][ruota] = {
        "ultima": ultime,
        "ambo": ambo,
        "score": round(score_ambo, 2)
    }

# ===== TOP 3 =====
top_sorted = sorted(
    risultati["ruote"].items(),
    key=lambda x: x[1]["score"],
    reverse=True
)

top3 = top_sorted[:3]

risultati["top"] = [t[0] for t in top3]

risultati["giocate"] = [
    {"ruota": r, "ambo": d["ambo"]}
    for r, d in top3
]

# ===== JOLLY INTELLIGENTE =====

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

# miglior ambo globale
miglior = max(risultati["ruote"].items(), key=lambda x: x[1]["score"])
ruota_origine = miglior[0]
ambo_top = miglior[1]["ambo"]

ruote_top = risultati["top"]

# scelta jolly
ruota_jolly = gemelle.get(ruota_origine, None)

if not ruota_jolly or ruota_jolly in ruote_top:
    alternative = [
        r for r in risultati["ruote"]
        if r not in ruote_top and r != ruota_origine
    ]

    if alternative:
        ruota_jolly = max(alternative, key=lambda r: risultati["ruote"][r]["score"])
    else:
        ruota_jolly = ruota_origine

risultati["jolly"] = {
    "ruota": ruota_jolly,
    "ambo": ambo_top
}

# ===== SALVA =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2)

print("🔥 SISTEMA FIXATO - DINAMICO ATTIVO")