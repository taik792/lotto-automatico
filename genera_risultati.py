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
    if len(estrazioni_ruota) < 20:
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

        # penalità se appena uscito
        penalita = 10 if n in ultime else 0

        # ultime 5 estrazioni
        ultime_5 = estrazioni_ruota[-5:]
        presenze_recenti = sum(1 for estr in ultime_5 if n in estr)

        # numeri vicini
        bonus_vicini = 0
        if n-1 in ultime or n+1 in ultime:
            bonus_vicini = 1

        # ===== SCORE BILANCIATO =====
        score = (
            freq_breve.get(n, 0) * 3 +
            freq_medio.get(n, 0) * 1.5 +
            freq_lungo.get(n, 0) * 1 +
            (ritardi[n] ** 1.2) * 0.5 +
            presenze_recenti * 2 +
            bonus_vicini * 1 -
            penalita
        )

        # boost ritardi alti
        if ritardi[n] > 20:
            score += ritardi[n] * 0.3

        # spike (forte breve + lungo)
        if freq_breve.get(n,0) > 2 and freq_lungo.get(n,0) > 15:
            score += 5

        # random leggero
        score += random.uniform(0, 0.5)

        score_num[n] = score

    # ===== CANDIDATI =====
    candidati = [n for n in range(1, 91) if n not in ultime]
    candidati.sort(key=lambda x: score_num[x], reverse=True)

    # ===== GENERAZIONE 3 AMBI DIVERSI =====
    top10 = candidati[:10]
    ambi = []
    usati = set()

    for n in top10:
        if n in usati:
            continue
        for m in top10:
            if m != n and m not in usati:
                ambi.append([n, m])
                usati.add(n)
                usati.add(m)
                break
        if len(ambi) == 3:
            break

    # score ruota (solo primo ambo)
    score_finale = round(score_num[ambi[0][0]] + score_num[ambi[0][1]], 2)

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

# ===== SALVATAGGIO =====
with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2)

print("🔥 ELITE COMPLETO ATTIVO")