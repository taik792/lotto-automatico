import random
from collections import defaultdict

# ================================
# CONFIG
# ================================
PESO_FREQ_COPPIA = 0.5
PESO_SCORE_SINGOLO = 0.3
PESO_RITARDO = 0.2

TOP_NUMERI = 10   # quanti numeri top usare
AMBI_FINALI = 20  # quanti ambi generare


# ================================
# MOCK DATI (SOSTITUISCI CON I TUOI)
# ================================

# score generale numeri (dal tuo algoritmo)
score_numeri = {i: random.uniform(0, 1) for i in range(1, 91)}

# ritardi (più alto = più ritardatario)
ritardi = {i: random.randint(0, 100) for i in range(1, 91)}

# frequenza coppie (simulata)
freq_coppie = defaultdict(lambda: defaultdict(int))

for i in range(1, 91):
    for j in range(1, 91):
        if i != j:
            freq_coppie[i][j] = random.randint(0, 20)


# ================================
# STEP 1 - PRENDI NUMERI TOP
# ================================
def get_top_numbers(score_numeri, ritardi, n=TOP_NUMERI):
    ranking = []

    for num in range(1, 91):
        score = (
            score_numeri[num] * 0.7 +
            (ritardi[num] / 100) * 0.3
        )
        ranking.append((num, score))

    ranking.sort(key=lambda x: x[1], reverse=True)

    return [num for num, _ in ranking[:n]]


# ================================
# STEP 2 - TROVA MIGLIOR COMPAGNO
# ================================
def trova_miglior_compagno(n1, score_numeri, ritardi, freq_coppie):
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


# ================================
# STEP 3 - GENERA AMBI
# ================================
def genera_ambi():
    ambi = []

    top_numbers = get_top_numbers(score_numeri, ritardi)

    for n1 in top_numbers:
        n2, score = trova_miglior_compagno(
            n1,
            score_numeri,
            ritardi,
            freq_coppie
        )

        if n2:
            ambi.append({
                "ambo": tuple(sorted([n1, n2])),
                "score": round(score, 4)
            })

    # ordina per qualità
    ambi.sort(key=lambda x: x["score"], reverse=True)

    return ambi[:AMBI_FINALI]


# ================================
# RUN
# ================================
if __name__ == "__main__":
    risultati = genera_ambi()

    print("\n🔥 AMBI GENERATI:\n")

    for r in risultati:
        print(f"{r['ambo']}  | score: {r['score']}")
