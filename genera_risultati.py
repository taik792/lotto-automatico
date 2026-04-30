import json
from itertools import combinations

RUOTE = ["Bari","Cagliari","Firenze","Genova","Milano","Napoli","Palermo","Roma","Torino","Venezia","Nazionale"]

# ===== CARICA DATI =====
with open("estrazioni.json", encoding="utf-8") as f:
    estrazioni = json.load(f)

risultati = {
    "top": [],
    "ruote": {},
    "giocate": [],
    "jolly": {}
}

# ===== FUNZIONI STATISTICHE =====
def calcola_freq(lista):
    freq = {}
    for estr in lista:
        for n in estr:
            freq[n] = freq.get(n, 0) + 1
    return freq

def calcola_cooccorrenze(lista):
    coppie = {}
    for estr in lista:
        for a, b in combinations(sorted(estr), 2):
            coppie[(a, b)] = coppie.get((a, b), 0) + 1
    return coppie

# ===== ANALISI RUOTE =====
for ruota in RUOTE:
    if ruota not in estrazioni:
        continue

    estrazioni_ruota = estrazioni[ruota]
    if len(estrazioni_ruota) < 50:
        continue

    ultime = estrazioni_ruota[-1]

    # --- NUOVI CICLI BILANCIATI ---
    breve = estrazioni_ruota[-18:]   # Ciclo naturale (18)
    medio = estrazioni_ruota[-540:]  # Stabilità 3 anni (540)
    lungo = estrazioni_ruota[-1000:] # Memoria storica (1000)

    freq_breve = calcola_freq(breve)
    freq_medio = calcola_freq(medio)
    freq_lungo = calcola_freq(lungo)

    # Co-occorrenze basate sul periodo medio per massima attendibilità
    cooc = calcola_cooccorrenze(medio)

    # ===== RITARDI =====
    ritardi = {}
    for n in range(1, 91):
        ritardo = 0
        for estr in reversed(estrazioni_ruota):
            if n in estr:
                break
            ritardo += 1
        ritardi[n] = ritardo

    # ===== SCORE NUMERI (PESI AGGIORNATI) =====
    score_num = {}
    ultime_5 = estrazioni_ruota[-5:]

    for n in range(1, 91):
        penalita = 10 if n in ultime else 0
        presenze_recenti = sum(1 for estr in ultime_5 if n in estr)
        bonus_vicini = 1 if (n-1 in ultime or n+1 in ultime) else 0

        # Formula bilanciata per i nuovi archi temporali
        score = (
            freq_breve.get(n, 0) * 2.5 +     # Peso sulla frequenza attuale
            freq_medio.get(n, 0) * 1.2 +     # Peso sulla costanza media
            freq_lungo.get(n, 0) * 0.8 +     # Peso sullo storico
            (ritardi[n] ** 1.15) * 0.6 + 
            presenze_recenti * 2 +
            bonus_vicini -
            penalita
        )

        if ritardi[n] > 20:
            score += ritardi[n] * 0.25

        if freq_breve.get(n, 0) > 2 and freq_lungo.get(n, 0) > 15:
            score += 5

        score_num[n] = score

    # ===== SCELTA AMBO INTELLIGENTE =====
    candidati = [n for n in range(1, 91) if n not in ultime]
    ritardatari = [n for n in candidati if ritardi[n] > 20]
    frequenti = [n for n in candidati if freq_breve.get(n, 0) >= 2]
    top_numeri = sorted(candidati, key=lambda x: score_num[x], reverse=True)[:20]

    miglior_ambo = None
    miglior_score = 0

    # Liste per i due tipi di ricerca (1. Mix Forzato, 2. Fallback)
    ricerche = [
        (ritardatari, frequenti, 1.0), 
        (top_numeri, top_numeri, 0.6) # 0.6 è la penalty se entrambi sono ritardatari
    ]

    for lista_a, lista_b, penalty_base in ricerche:
        if miglior_ambo and lista_a == top_numeri: break # Se abbiamo già un ambo dal mix, saltiamo il fallback
        
        for a, b in combinations(set(lista_a + lista_b), 2):
            if a == b: continue
            
            # Controllo: se entrambi sono super-ritardatari nel fallback, applica penalty
            penalty = penalty_base
            if lista_a == top_numeri and ritardi[a] > 25 and ritardi[b] > 25:
                penalty = 0.6

            base = score_num[a] + score_num[b]
            coppia = tuple(sorted((a, b)))
            co_score = cooc.get(coppia, 0)

            # POTENZIAMENTO CO-OCCORRENZE (x8)
            score_finale = (base + co_score * 8) * penalty

            # FILTRO SICUREZZA: Ambo non uscito negli ultimi 50 turni
            ambo_recente = False
            for estr in estrazioni_ruota[-50:]:
                if a in estr and b in estr:
                    ambo_recente = True
                    break
            if ambo_recente:
                score_finale *= 0.5

            if score_finale > miglior_score:
                miglior_score = score_finale
                miglior_ambo = [a, b]

    risultati["ruote"][ruota] = {
        "ultima": ultime,
        "ambo": miglior_ambo,
        "score": round(miglior_score, 2)
    }

# ===== GESTIONE TOP 3 E JOLLY (RESTO DEL CODICE INVARIATO) =====
top_sorted = sorted(risultati["ruote"].items(), key=lambda x: x[1]["score"], reverse=True)
top3 = top_sorted[:3]
risultati["top"] = [t[0] for t in top3]

for ruota, dati in top3:
    risultati["giocate"].append({"ruota": ruota, "ambo": dati["ambo"]})

gemelle = {"Bari":"Napoli","Napoli":"Bari","Milano":"Torino","Torino":"Milano","Palermo":"Cagliari","Cagliari":"Palermo","Firenze":"Genova","Genova":"Firenze"}
miglior_ambo_assoluto = top_sorted[0][1]["ambo"]
ruota_origine = top_sorted[0][0]
ruota_jolly = gemelle.get(ruota_origine)

if not ruota_jolly or ruota_jolly in risultati["top"]:
    candidati_j = [r for r in risultati["ruote"] if r != ruota_origine and r not in risultati["top"]]
    ruota_jolly = max(candidati_j, key=lambda r: risultati["ruote"][r]["score"]) if candidati_j else ruota_origine

risultati["jolly"] = {"ruota": ruota_jolly, "ambo": miglior_ambo_assoluto}

with open("risultati.json", "w", encoding="utf-8") as f:
    json.dump(risultati, f, indent=2)

print("🔥 MOTORE PRO V2 AGGIORNATO (18/540/1000 + CO-OCCORRENZE X8)")
