from collections import Counter
from utils import prendi_ultime_estrazioni, prendi_recenti

def analizza_ruote(dati):
    risultato = []
    giocate_top = []

    for ruota, estrazioni in dati.items():

        estrazioni_lungo = prendi_ultime_estrazioni(estrazioni)
        estrazioni_breve = prendi_recenti(estrazioni)

        if len(estrazioni_lungo) < 5:
            continue

        ultima = estrazioni_lungo[-1]

        # 🔥 FREQUENZE LUNGO
        freq = Counter()
        for estr in estrazioni_lungo:
            freq.update(estr)

        # 🔥 NUMERI RECENTI (ATTIVI)
        recenti = set()
        for estr in estrazioni_breve:
            recenti.update(estr)

        # 🔥 ORDINA PER FREQUENZA
        ordinati = sorted(freq, key=freq.get, reverse=True)

        # 🔥 FILTRO INTELLIGENTE
        numeri_caldi = [
            n for n in ordinati
            if n not in ultima and n in recenti
        ][:2]

        # fallback
        if len(numeri_caldi) < 2:
            numeri_caldi = ordinati[:2]

        # 🔥 AMBO
        ambo = f"{numeri_caldi[0]}-{numeri_caldi[1]}"

        # 🔥 CICLOMETRIA
        ciclo = []
        for n in numeri_caldi:
            distanza = 0
            for estr in reversed(estrazioni_lungo):
                if n in estr:
                    break
                distanza += 1
            ciclo.append(distanza)

        ciclometria = f"{ciclo[0]} | {ciclo[1]}"

        # 🔥 SATURAZIONE
        saturazione = round(sum(freq.values()) / len(freq), 2)

        # 🔥 INDICE (NUOVO)
        indice_val = round(
            (freq[numeri_caldi[0]] + freq[numeri_caldi[1]]) /
            (1 + ciclo[0] + ciclo[1]),
            2
        )

        risultato.append({
            "ruota": ruota,
            "ultima": ultima,
            "numeri_caldi": numeri_caldi,
            "ambo_forte": ambo,
            "ciclometria": ciclometria,
            "saturazione": saturazione,
            "indice": indice_val
        })

        giocate_top.append({
            "ruota": ruota,
            "ambo": ambo,
            "score": indice_val
        })

    # 🔥 TOP 3 REALI
    giocate_top = sorted(giocate_top, key=lambda x: x["score"], reverse=True)[:3]

    return risultato, giocate_top