import json
import random

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia"]

with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {
    "top": [],
    "ruote": {}
}

def calcola_freq(lista):
    freq = {}
    for estr in lista:
        for n in estr:
            freq[n] = freq.get(n, 0) + 1
    return freq

for ruota in RUOTE:

    if ruota not in estrazioni:
        continue

    estrazioni_ruota = estrazioni[ruota]
    if len(estrazioni_ruota) < 10:
        continue

    ultime = estrazioni_ruota[-1]

    breve = estrazioni_ruota[-20:]
    medio = estrazioni_ruota[-100:]
    lungo = estrazioni_ruota[-500:]

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

        # penalità recenti
        penalita = 0
        if n in ultime:
            penalita = 10

        # presenza ultime 5
        ultime_5 = estrazioni_ruota[-5:]
        presenze_recenti = sum(1 for estr in ultime_5 if n in estr)

        # vicinanza numeri
        vicini = [n-1, n+1]
        bonus_vicini = sum(1 for v in vicini if v in ultime)

        score = (
            freq_breve.get(n, 0) * 4 +
            freq_medio.get(n, 0) * 2 +
            freq_lungo.get(n, 0) * 1.5 +
            (ritardi[n] ** 1.3) * 0.8 +
            presenze_recenti * 3 +
            bonus_vicini * 2 -
            penalita
        )

        # boost ritardi forti
        if ritardi[n] > 20:
            score += ritardi[n] * 0.5

        # spike (numero forte breve + lungo)
        if freq_breve.get(n,0) > 2 and freq_lungo.get(n,0) > 15:
            score += 10

        # random leggero
        score += random.uniform(0, 1.5)

        score_num[n] = score

    # ===== CANDIDATI =====
    candidati = [n for n in range(1, 91) if n not in ultime]
    candidati.sort(key=lambda x: score_num[x], reverse=True)

    top6 = candidati[:6]

    # ===== 3 AMBI =====
    ambi = [
        [top6[0], top6[1]],  # forte
        [top6[2], top6[3]],  # medio
        [top6[4], top6[5]]   # copertura
    ]

    score_finale = round(sum(score_num[n] for n in top6[:2]), 2)

    risultati["ruote"][ruota] = {
        "ultima": ultime,
        "ambi": ambi,
        "score": score_finale
    }

# ===== TOP =====
top_sorted = sorted(
    risultati["ruote"].items(),
    key=lambda x: x[1]["score"],
    reverse=True
)

risultati["top"] = [t[0] for t in top_sorted[:5]]

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2)

print("🔥 ELITE MODE ATTIVO")