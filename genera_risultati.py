import json

# Carica dati
with open("estrazioni.json") as f:
    estrazioni = json.load(f)

risultati = {}

def frequenza(num, storico):
    count = 0
    for estr in storico[-20:]:
        if num in estr:
            count += 1
    return count

def ritardo(num, storico):
    for i, estr in enumerate(reversed(storico)):
        if num in estr:
            return i + 1
    return 50

for ruota, storico in estrazioni.items():

    ultima = storico[-1]

    # numeri candidati (ultimi 3 concorsi)
    candidati = []
    for estr in storico[-3:]:
        candidati.extend(estr)

    candidati = list(set(candidati))

    migliori = []

    for n in candidati:
        f = frequenza(n, storico)
        r = ritardo(n, storico)

        score = (f * 2) + r

        migliori.append((n, score))

    migliori.sort(key=lambda x: x[1], reverse=True)

    # prendi top 2 numeri
    top2 = [migliori[0][0], migliori[1][0]]
    score_finale = migliori[0][1] + migliori[1][1]

    risultati[ruota] = {
        "ruota": ruota,
        "ambo": top2,
        "score": round(score_finale, 2)
    }

# 🔥 FILTRO FORTE
filtrati = dict(
    sorted(risultati.items(), key=lambda x: x[1]["score"], reverse=True)[:5]
)

with open("risultati.json", "w") as f:
    json.dump(filtrati, f, indent=2)

print("\n--- SEGNALI TOP ---\n")