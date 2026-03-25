from collections import Counter
from utils import prendi_ultime_estrazioni, prendi_recenti

# 🔥 CICLOMETRIA REALE (media tra uscite)
def calcola_ciclo_reale(numero, estrazioni):
    posizioni = []

    for i, estr in enumerate(estrazioni):
        if numero in estr:
            posizioni.append(i)

    # se esce troppo poco → ciclo 0
    if len(posizioni) < 2:
        return 0

    # distanza tra uscite
    distanze = []
    for i in range(1, len(posizioni)):
        distanze.append(posizioni[i] - posizioni[i - 1])

    # media
    return int(sum(distanze) / len(distanze))


def analizza_ruote(dati):
    risultato = []
    giocate_top = []

    for ruota, estrazioni in dati.items():

        estrazioni_lungo = prendi_ultime_estrazioni(estrazioni)
        estrazioni_breve = prendi_recenti(estrazioni)

        if len(estrazioni_lungo) < 10:
            continue

        ultima = estrazioni_lungo[-1]

        # 🔥 FREQUENZA
        freq = Counter()
        for estr in estrazioni_lungo:
            freq.update(estr)

        # 🔥 NUMERI RECENTI (attivi)
        recenti = set()
        for estr in estrazioni_breve:
            recenti.update(estr)

        # 🔥 ORDINA PER FREQUENZA
        ordinati = sorted(freq, key=freq.get, reverse=True)

        # 🔥 FILTRO (no ultima + presenti nel breve)
        numeri_caldi = [
            n for n in ordinati
            if n not in ultima and n in recenti
        ][:2]

        # fallback
        if len(numeri_caldi) < 2:
            numeri_caldi = ordinati[:2]

        # 🔥 AMBO
        ambo = f"{numeri_caldi[0]}-{numeri_caldi[1]}"

        # 🔥 CICLO REALE
        ciclo_vals = []
        for n in numeri_caldi:
            ciclo_vals.append(calcola_ciclo_reale(n, estrazioni_lungo))

        ciclometria = f"{ciclo_vals[0]} | {ciclo_vals[1]}"

        # 🔥 SATURAZIONE (più corretta)
        totale_numeri = sum(freq.values())
        numeri_unici = len(freq)
        saturazione = round(totale_numeri / numeri_unici / 10, 2)

        # 🔥 INDICE INTELLIGENTE
        indice = round(
            (freq[numeri_caldi[0]] + freq[numeri_caldi[1]]) /
            (1 + ciclo_vals[0] + ciclo_vals[1]),
            2
        )

        risultato.append({
            "ruota": ruota,
            "ultima": ultima,
            "numeri_caldi": numeri_caldi,
            "ambo_forte": ambo,
            "ciclometria": ciclometria,
            "saturazione": saturazione,
            "indice": indice
        })

        giocate_top.append({
            "ruota": ruota,
            "ambo": ambo,
            "score": indice
        })

    # 🔥 TOP 3
    giocate_top = sorted(giocate_top, key=lambda x: x["score"], reverse=True)[:3]

    return risultato, giocate_top