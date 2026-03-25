from utils import prendi_ultime_estrazioni
from collections import Counter


def analizza_ruote(dati):
    risultato = []

    for ruota, estrazioni in dati.items():

        # 🔥 PRENDI SOLO LE ULTIME
        estrazioni = prendi_ultime_estrazioni(estrazioni)

        if len(estrazioni) < 2:
            continue

        ultima = estrazioni[-1]

        # 🔢 FLATTEN NUMERI
        numeri = [n for estr in estrazioni for n in estr]

        # 📊 FREQUENZA
        freq = Counter(numeri)

        # 🔥 ORDINA PER FREQUENZA
        ordinati = sorted(freq, key=freq.get, reverse=True)

        # ❌ ESCLUDI NUMERI APPENA USCITI
        numeri_caldissimi = [n for n in ordinati if n not in ultima]

        # 🎯 PRENDI I MIGLIORI 2
        numeri_caldissimi = numeri_caldissimi[:2]

        # 🛟 BACKUP
        if len(numeri_caldissimi) < 2:
            for n in ordinati:
                if n not in numeri_caldissimi:
                    numeri_caldissimi.append(n)
                if len(numeri_caldissimi) == 2:
                    break

        # 💣 AMBO
        ambo = f"{numeri_caldissimi[0]}-{numeri_caldissimi[1]}"

        # 🔁 CICLOMETRIA (DISTANZA REALE)
        ciclometria = []
        for num in numeri_caldissimi:
            distanza = 0
            for estr in reversed(estrazioni):
                distanza += 1
                if num in estr:
                    break
            ciclometria.append(distanza)

        # 📉 SATURAZIONE CORRETTA
        valori_freq = [freq[n] for n in numeri_caldissimi]
        tot_numeri = len(estrazioni) * 5
        saturazione = round((sum(valori_freq) / tot_numeri) * 10, 2)

        risultato.append({
            "ruota": ruota,
            "ultima": ultima,
            "numeri_caldi": numeri_caldissimi,
            "ambo_forte": ambo,
            "ciclometria": ciclometria,
            "saturazione": saturazione
        })

    return risultato