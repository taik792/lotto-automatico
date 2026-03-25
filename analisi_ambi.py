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

        # 🔢 FLATTEN (tutti i numeri)
        numeri = [n for estr in estrazioni for n in estr]

        # 📊 FREQUENZA
        freq = Counter(numeri)

        # 🔥 NUMERI ORDINATI PER FREQUENZA
        ordinati = sorted(freq, key=freq.get, reverse=True)

        # ❌ ESCLUDI ULTIMA ESTRAZIONE
        numeri_caldissimi = [n for n in ordinati if n not in ultima]

        # 🎯 PRENDI I MIGLIORI 2
        numeri_caldissimi = numeri_caldissimi[:2]

        # 🛟 BACKUP se non bastano
        if len(numeri_caldissimi) < 2:
            for n in ordinati:
                if n not in numeri_caldissimi:
                    numeri_caldissimi.append(n)
                if len(numeri_caldissimi) == 2:
                    break

        # 💣 AMBO
        ambo = f"{numeri_caldissimi[0]}-{numeri_caldissimi[1]}"

        # 🔁 CICLOMETRIA BASE (distanza ultima uscita)
        ciclometria = []
        for num in numeri_caldissimi:
            distanza = 0
            for estr in reversed(estrazioni):
                distanza += 1
                if num in estr:
                    break
            ciclometria.append(distanza)

        # 📉 SATURAZIONE (media frequenze normalizzata)
        valori