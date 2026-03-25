from collections import Counter
from utils import prendi_ultime_estrazioni

def analizza_ruote(dati):
    risultato = []

    for ruota, estrazioni in dati.items():

        # 🔥 NORMALIZZA DATI (qualsiasi formato JSON)
        estrazioni_pulite = []

        for e in estrazioni:
            if isinstance(e, dict):
                if "numeri" in e:
                    estrazioni_pulite.append([int(x) for x in e["numeri"]])
            elif isinstance(e, list):
                estrazioni_pulite.append([int(x) for x in e])

        # PRENDI SOLO LE ULTIME N
        ultime = prendi_ultime_estrazioni(estrazioni_pulite)

        if len(ultime) < 2:
            continue

        # 📌 ULTIMA ESTRAZIONE
        ultima = ultime[-1]

        # 🔥 FREQUENZA NUMERI
        freq = Counter()
        for estr in ultime:
            freq.update(estr)

        # 🔥 ORDINA NUMERI CALDI
        ordinati = sorted(freq, key=freq.get, reverse=True)

        # ❌ ESCLUDI NUMERI ULTIMA ESTRAZIONE
        numeri_caldi = [n for n in ordinati if n not in ultima][:2]

        # fallback sicurezza
        if len(numeri_caldi) < 2:
            numeri_caldi = ordinati[:2]

        # 🎯 AMBO
        ambo = f"{numeri_caldi[0]}-{numeri_caldi[1]}"

        # 🔁 CICLOMETRIA (ritardo)
        def ritardo(numero):
            count = 0
            for estr in reversed(ultime):
                if numero in estr:
                    return count
                count += 1
            return count

        ciclo1 = ritardo(numeri_caldi[0])
        ciclo2 = ritardo(numeri_caldi[1])

        # 📊 SATURAZIONE (frequenza relativa)
        totale = sum(freq.values())
        sat = (freq[numeri_caldi[0]] + freq[numeri_caldi[1]]) / totale if totale > 0 else 0

        risultato.append({
            "ruota": ruota,
            "ultima": ultima,
            "numeri_caldi": numeri_caldi,
            "ambo_forte": ambo,
            "ciclometria": f"{ciclo1} | {ciclo2}",
            "saturazione": round(sat * 10, 2)  # scala più leggibile
        })

    return risultato