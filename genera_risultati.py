import json

LUNGO = 200
MEDIO = 80
BREVE = 20

with open("estrazioni.json", "r") as f:
    data = json.load(f)

ruote_nomi = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia"
]

# 🔥 CONVERTI IN LISTA ESTRAZIONI
estrazioni = []

# prende lunghezza massima
max_len = len(data[ruote_nomi[0]])

for i in range(max_len):
    estrazione = {}
    for r in ruote_nomi:
        estrazione[r] = data[r][i]
    estrazioni.append(estrazione)

# 📊 ritardi
def calcola_ritardi(ruota, window):
    conteggio = {n: 0 for n in range(1, 91)}

    ultime = estrazioni[-window:] if len(estrazioni) >= window else estrazioni

    for estrazione in ultime:
        usciti = estrazione[ruota]
        for n in conteggio:
            if n not in usciti:
                conteggio[n] += 1

    return conteggio

# 🎯 score
def score_numeri(ruota):
    r1 = calcola_ritardi(ruota, LUNGO)
    r2 = calcola_ritardi(ruota, MEDIO)
    r3 = calcola_ritardi(ruota, BREVE)

    score = {}
    for n in range(1, 91):
        score[n] = r1[n]*0.5 + r2[n]*0.3 + r3[n]*0.2

    return score

ruote = {}
ranking = []

for ruota in ruote_nomi:
    score = score_numeri(ruota)

    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[:6]
    nums = [n for n, _ in top]

    ambi = []
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            ambi.append((nums[i], nums[j], score[nums[i]] + score[nums[j]]))

    ambi.sort(key=lambda x: x[2], reverse=True)
    best = ambi[0]

    ruote[ruota] = {
        "ultima": estrazioni[-1][ruota],
        "ambo": [best[0], best[1]],
        "score": round(best[2], 2)
    }

    ranking.append((ruota, best[2]))

ranking.sort(key=lambda x: x[1], reverse=True)

top3 = [r for r, _ in ranking[:3]]
altre = [r for r, _ in ranking if r not in top3]

jolly = altre[0]

output = {
    "top": top3,
    "jolly": jolly,
    "ruote": ruote
}

with open("risultati.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ OK GENERATO")