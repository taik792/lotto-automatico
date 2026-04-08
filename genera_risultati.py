import json
import random

# 🔧 PARAMETRI FINESTRE (puoi cambiare)
LUNGO = 200
MEDIO = 80
BREVE = 20

# 📥 Carica estrazioni
with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

ruote_nomi = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia"
]

# 📊 Funzione ritardi
def calcola_ritardi(ruota, window):
    conteggio = {n: 0 for n in range(1, 91)}

    for estrazione in estrazioni[-window:]:
        usciti = estrazione.get(ruota, [])
        for n in conteggio:
            if n not in usciti:
                conteggio[n] += 1

    return conteggio

# 🎯 Score combinato (VERO MOTORE)
def score_numeri(ruota):
    r_lungo = calcola_ritardi(ruota, LUNGO)
    r_medio = calcola_ritardi(ruota, MEDIO)
    r_breve = calcola_ritardi(ruota, BREVE)

    score = {}
    for n in range(1, 91):
        score[n] = (
            r_lungo[n] * 0.5 +
            r_medio[n] * 0.3 +
            r_breve[n] * 0.2
        )

    return score

# 🧠 Calcolo ambi per ogni ruota
ruote = {}
top_ruote = []

for ruota in ruote_nomi:
    score = score_numeri(ruota)

    # Prendi top 6 numeri
    numeri_ordinati = sorted(score.items(), key=lambda x: x[1], reverse=True)
    top_numeri = [n for n, _ in numeri_ordinati[:6]]

    # Genera ambi possibili
    ambi = []
    for i in range(len(top_numeri)):
        for j in range(i+1, len(top_numeri)):
            ambi.append((top_numeri[i], top_numeri[j]))

    # Prendi il migliore (somma score)
    ambi_score = []
    for a, b in ambi:
        ambi_score.append(((a, b), score[a] + score[b]))

    ambi_score.sort(key=lambda x: x[1], reverse=True)
    best_ambo = ambi_score[0][0]
    best_score = ambi_score[0][1]

    ruote[ruota] = {
        "ultima": estrazioni[-1][ruota],
        "ambo": list(best_ambo),
        "score": round(best_score, 2)
    }

    top_ruote.append((ruota, best_score))

# 🔥 TOP 3 RUOTE
top_ruote.sort(key=lambda x: x[1], reverse=True)
top3 = [r for r, _ in top_ruote[:3]]

# 💣 JOLLY = ruota fuori top ma con score alto
altre = [r for r, _ in top_ruote if r not in top3]
jolly_ruota = altre[0]

# 📦 OUTPUT FINALE
output = {
    "top": top3,
    "jolly": jolly_ruota,
    "ruote": ruote
}

# 💾 Salva
with open("risultati.json", "w") as f:
    json.dump(output, f, indent=2)

print("✅ RISULTATI GENERATI")