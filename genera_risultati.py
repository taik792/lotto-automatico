import json
import random
from collections import defaultdict

# ================================
# CONFIG
# ================================
PESO_FREQ_COPPIA = 0.5
PESO_SCORE_SINGOLO = 0.3
PESO_RITARDO = 0.2

TOP_NUMERI = 10
AMBI_FINALI = 20


# ================================
# MOCK DATI (SOSTITUISCI)
# ================================
score_numeri = {i: random.uniform(0, 1) for i in range(1, 91)}
ritardi = {i: random.randint(0, 100) for i in range(1, 91)}

freq_coppie = defaultdict(lambda: defaultdict(int))
for i in range(1, 91):
    for j in range(1, 91):
        if i != j:
            freq_coppie[i][j] = random.randint(0, 20)


# ================================
# LOGICA
# ================================
def get_top_numbers():
    ranking = []

    for num in range(1, 91):
        score = (
            score_numeri[num] * 0.7 +
            (ritardi[num] / 100) * 0.3
        )
        ranking.append((num, score))

    ranking.sort(key=lambda x: x[1], reverse=True)
    return [num for num, _ in ranking[:TOP_NUMERI]]


def trova_miglior_compagno(n1):
    best_score = -1
    best_num = None

    for n2 in range(1, 91):
        if n2 == n1:
            continue

        score = (
            freq_coppie[n1][n2] * PESO_FREQ_COPPIA +
            score_numeri[n2] * PESO_SCORE_SINGOLO +
            (ritardi[n2] / 100) * PESO_RITARDO
        )

        if score > best_score:
            best_score = score
            best_num = n2

    return best_num, best_score


def genera_ambi():
    ambi = []
    top_numbers = get_top_numbers()

    for n1 in top_numbers:
        n2, score = trova_miglior_compagno(n1)

        if n2:
            ambi.append({
                "ambo": sorted([n1, n2]),
                "score": round(score, 4)
            })

    ambi.sort(key=lambda x: x["score"], reverse=True)
    return ambi[:AMBI_FINALI]


# ================================
# SALVATAGGIO JSON 🔥
# ================================
def salva_risultati(ambi):
    data = {
        "ambi": ambi
    }

    with open("risultati.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ risultati.json aggiornato")


# ================================
# RUN
# ================================
if __name__ == "__main__":
    risultati = genera_ambi()

    salva_risultati(risultati)

    print("\n🔥 AMBI GENERATI:\n")
    for r in risultati:
        print(f"{r['ambo']}  | score: {r['score']}")