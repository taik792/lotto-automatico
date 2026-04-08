import json
from collections import Counter

# =========================
# ⚙️ CONFIG
# =========================
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

# =========================
# 📥 CARICAMENTO SICURO
# =========================
with open("estrazioni.json") as f:
    raw = json.load(f)

if isinstance(raw, list):
    estrazioni = raw
elif isinstance(raw, dict):
    if "estrazioni" in raw:
        estrazioni = raw["estrazioni"]
    else:
        estrazioni = list(raw.values())
else:
    raise Exception("Formato estrazioni.json non valido")

estrazioni = list(estrazioni)[-LUNGO:]


# =========================
# 🔢 RITARDI UNIVERSALI
# =========================
def get_numeri(estr, ruota):
    if isinstance(estr, dict):
        return estr.get(ruota, [])
    return estr  # fallback lista semplice


def calcola_ritardi(ruota, window):
    ritardi = {n: 0 for n in range(1, 91)}
    subset = estrazioni[-window:]

    for numero in range(1, 91):
        ritardo = 0

        for estr in reversed(subset):
            numeri = get_numeri(estr, ruota)

            if numero in numeri:
                break

            ritardo += 1

        ritardi[numero] = ritardo

    return ritardi


# =========================
# 🔗 COPPIE
# =========================
def frequenze_coppie(ruota):
    c = Counter()

    for estr in estrazioni:
        nums = sorted(get_numeri(estr, ruota))

        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                c[(nums[i], nums[j])] += 1

    return c


# =========================
# 🚀 CALCOLO PRINCIPALE
# =========================
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

    numeri = sorted(score, key=score.get, reverse=True)[:12]
    c = frequenze_coppie(ruota)

    # =========================
    # 🎯 AMBO REALISTICO
    # =========================
    best_ambo = None
    best_score = -999

    for i in range(len(numeri)):
        for j in range(i+1, len(numeri)):

            a, b = sorted((numeri[i], numeri[j]))
            distanza = abs(a - b)

            pair_score = score[a] + score[b]

            pair_score += c.get((a, b), 0) * 4

            if 5 <= distanza <= 45:
                pair_score += 15
            else:
                pair_score -= 20

            if distanza < 3:
                pair_score -= 10

            if (a % 2) != (b % 2):
                pair_score += 5

            if pair_score > best_score:
                best_score = pair_score
                best_ambo = (a, b)

    # ultimi numeri
    ultimi = get_numeri(estrazioni[-1], ruota)

    score_ruota = sum(score[n] for n in numeri[:5])

    ranking.append((ruota, score_ruota))

    risultati[ruota] = {
        "ultimi": ultimi,
        "ambo": list(best_ambo),
        "score": round(score_ruota, 2)
    }


# =========================
# 🏆 TOP + JOLLY
# =========================
top3 = sorted(ranking, key=lambda x: x[1], reverse=True)[:3]
top3_ruote = [r[0] for r in top3]

prima = top3_ruote[0]
jolly = GEMELLE.get(prima, top3_ruote[1])


# =========================
# 💾 OUTPUT
# =========================
output = {
    "top": top3_ruote,
    "jolly": jolly,
    "ruote": risultati
}

with open("risultati.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ GENERATO PRO V3 ULTRA FIX")