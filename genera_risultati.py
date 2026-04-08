import json
from collections import defaultdict

LUNGO = 200
MEDIO = 80
BREVE = 30

with open("estrazioni.json", "r") as f:
    data = json.load(f)

ruote_nomi = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia"
]

# 🔁 CONVERSIONE
estrazioni = []
max_len = len(data[ruote_nomi[0]])

for i in range(max_len):
    estrazione = {}
    for r in ruote_nomi:
        estrazione[r] = data[r][i]
    estrazioni.append(estrazione)

# 📊 RITARDO
def ritardi(ruota, window):
    rit = {n: 0 for n in range(1, 91)}
    ultime = estrazioni[-window:]

    for estrazione in ultime:
        usciti = estrazione[ruota]
        for n in rit:
            if n not in usciti:
                rit[n] += 1

    return rit

# 📈 FREQUENZA
def frequenze(ruota, window):
    freq = {n: 0 for n in range(1, 91)}
    ultime = estrazioni[-window:]

    for estrazione in ultime:
        for n in estrazione[ruota]:
            freq[n] += 1

    return freq

# 🤝 COPPIE
def coppie(ruota, window):
    coppie_count = defaultdict(int)
    ultime = estrazioni[-window:]

    for estrazione in ultime:
        nums = estrazione[ruota]
        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                a, b = sorted((nums[i], nums[j]))
                coppie_count[(a, b)] += 1

    return coppie_count

ruote = {}
ranking = []

for ruota in ruote_nomi:

    r = ritardi(ruota, LUNGO)
    f = frequenze(ruota, BREVE)
    c = coppie(ruota, MEDIO)

    score = {}

    for n in range(1, 91):
        score[n] = (
            r[n] * 0.6 +       # ritardo
            f[n] * 0.3 -       # frequenza recente
            (0 if r[n] < 5 else 5)  # penalità numeri morti
        )

    # top numeri filtrati
    top = sorted(score.items(), key=lambda x: x[1], reverse=True)[:12]
    numeri = [n for n, _ in top]

    # 🔥 selezione AMBO INTELLIGENTE
    best_ambo = None
    best_score = -999

    for i in range(len(numeri)):
        for j in range(i+1, len(numeri)):

            a, b = sorted((numeri[i], numeri[j]))

            pair_score = (
                score[a] + score[b] +
                c.get((a, b), 0) * 5   # peso coppie reali
            )

            # evita numeri troppo distanti
            if abs(a - b) > 70:
                pair_score -= 10

            if pair_score > best_score:
                best_score = pair_score
                best_ambo = (a, b)

    ruote[ruota] = {
        "ultima": estrazioni[-1][ruota],
        "ambo": list(best_ambo),
        "score": round(best_score, 2)
    }

    ranking.append((ruota, best_score))

# 🔥 TOP
ranking.sort(key=lambda x: x[1], reverse=True)
top3 = [r for r, _ in ranking[:3]]

# 💣 JOLLY intelligente (ruota non top con coppie forti)
altre = [r for r, _ in ranking if r not in top3]
jolly = altre[0]

output = {
    "top": top3,
    "jolly": jolly,
    "ruote": ruote
}

with open("risultati.json", "w") as f:
    json.dump(output, f, indent=2)

print("🔥 PRO V2 ATTIVO")