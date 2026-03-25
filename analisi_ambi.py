from collections import Counter
from utils import prendi_ultime_estrazioni

# 🔥 NUOVA SATURAZIONE INTELLIGENTE
def calcola_saturazione(freq, numeri_caldi):
    if not numeri_caldi:
        return 0

    valori = [freq.get(n, 0) for n in numeri_caldi]
    media = sum(valori) / len(valori)
    max_freq = max(freq.values()) if freq else 1

    saturazione = media / max_freq

    return round(saturazione * 3, 2)


def analizza_ruote(dati):
    risultato = []

    for ruota, estrazioni in dati.items():

        # 🔥 PRENDI SOLO LE ULTIME
        estrazioni = prendi_ultime_estrazioni(estrazioni)

        if len(estrazioni) < 2:
            continue

        ultima = estrazioni[-1]

        # 🔢 FREQUENZA NUMERI
        freq = Counter()

        for estrazione in estrazioni:
            for n in estrazione:
                freq[n] += 1

        # 🔥 NUMERI CALDI (escludi ultima)
        ordinati = sorted(freq, key=freq.get, reverse=True)
        numeri_caldi = [n for n in ordinati if n not in ultima][:2]

        if len(numeri_caldi) < 2:
            numeri_caldi = ordinati[:2]

        # 🎯 AMBO FORTE
        ambo = f"{numeri_caldi[0]}-{numeri_caldi[1]}"

        # 🔄 CICLOMETRIA (semplice ma stabile)
        ciclometria = []
        for n in numeri_caldi:
            distanza = 0
            for estrazione in reversed(estrazioni):
                distanza += 1
                if n in estrazione:
                    break
            ciclometria.append(distanza)

        ciclometria_str = f"{ciclometria[0]} | {ciclometria[1]}"

        # 🔥 SATURAZIONE NUOVA
        saturazione = calcola_saturazione(freq, numeri_caldi)

        risultato.append({
            "ruota": ruota,
            "ultima": ultima,
            "numeri_caldi": numeri_caldi,
            "ambo_forte": ambo,
            "ciclometria": ciclometria_str,
            "saturazione": saturazione
        })

    return risultato