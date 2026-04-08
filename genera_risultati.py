import json
from collections import Counter

# ⚙️ CONFIG
LUNGO = 500
MEDIO = 200
BREVE = 50

PESO_LUNGO = 1
PESO_MEDIO = 2
PESO_BREVE = 3

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia"]

GEMELLE = {
    "Bari": "Cagliari",
    "Cagliari": "Bari",
    "Firenze": "Genova",
    "Genova": "Firenze",
    "Milano": "Napoli",
    "Napoli": "Milano",
    "Palermo": "Roma",
    "Roma": "Palermo",
    "Torino": "Venezia",
    "Venezia": "Torino"
}


# 📥 carica estrazioni
with open("estrazioni.json") as f:
    data = json.load(f)

estrazioni = data[-LUNGO:]  # prendiamo ultime N


# 🔢 calcolo ritardi
def calcola_ritardi(ruota, window):
    ritardi = {n: 0 for n in range(1, 91)}

    subset = estrazioni[-window:]

    for numero in range(1, 91):
        ritardo = 0
        for estr in reversed(subset):
            if numero in estr[ruota]:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    return ritardi


# 🔗 frequenze coppie
def frequenze_coppie(ruota):
    c = Counter()
    for estr in estrazioni:
        nums = sorted(estr[ruota])
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                c[(nums[i], nums[j])] += 1
    return c


risultati = {}
ranking = []

for ruota in RUOTE:

    r_lungo = calcola_ritardi(ruota, LUNGO)
    r_medio = calcola_ritardi(ruota, MEDIO)
    r_breve = calcola_ritardi(ruota, BREVE)

    score = {}

    for n in range(1, 91):
        score[n] = (
            r_lungo[n] * PESO_LUNGO +
            r_medio[n] * PESO_MEDIO +
            r_breve[n] * PESO_BREVE
        )

    # 🔝 top numeri
    numeri = sorted(score, key=score.get, reverse=True)[:12]

    # 🔗 coppie
    c = frequenze_coppie(ruota)

    # 🎯 selezione AMBO REALISTICO
    best_ambo = None
    best_score = -999

    for i in range(len(numeri)):
        for j in range(i+1, len(numeri)):

            a, b = sorted((numeri[i], numeri[j]))
            distanza = abs(a - b)

            pair_score = score[a] + score[b]

            # bonus coppia vista
            pair_score += c.get((a, b), 0) * 4

            # distanza ideale
            if 5 <= distanza <= 45:
                pair_score += 15
            else:
                pair_score -= 20

            # troppo vicini
            if distanza < 3:
                pair_score -= 10

            # pari/dispari
            if (a % 2) != (b % 2):
                pair_score += 5

            if pair_score > best_score:
                best_score = pair_score
                best_ambo = (a, b)

    # 📊 score ruota
    score_ruota = sum(score[n] for n in numeri[:5])

    ranking.append((ruota, score_ruota))

    risultati[ruota] = {
        "ultimi": estrazioni[-1][ruota],
        "ambo": list(best_ambo),
        "score": round(score_ruota, 2)
    }


# 🏆 TOP 3
top3 = sorted(ranking, key=lambda x: x[1], reverse=True)[:3]
top3_ruote = [r[0] for r in top3]

# 💣 JOLLY = gemella della prima
prima = top3_ruote[0]
jolly = GEMELLE.get(prima, top3_ruote[1])


# 💾 salva JSON
output = {
    "top": top3_ruote,
    "jolly": jolly,
    "ruote": risultati
}

with open("risultati.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ Generato PRO V3")