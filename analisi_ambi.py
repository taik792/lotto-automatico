from utils import prendi_ultime_estrazioni

def analizza_ruote(dati):
    risultato = []

    for ruota, estrazioni in dati.items():

        # 🔥 PRENDI SOLO LE ULTIME
        estrazioni = prendi_ultime_estrazioni(estrazioni)

        if len(estrazioni) < 2:
            continue

        ultima = estrazioni[-1]

        # 🔢 FLATTEN NUMERI
        numeri = []
        for estr in estrazioni:
            numeri.extend(estr)

        # 📊 FREQUENZE
        freq = {}
        for n in numeri:
            freq[n] = freq.get(n, 0) + 1

        # 🔥 NUMERI CALDI (ordinati)
        ordinati = sorted(freq, key=freq.get, reverse=True)

        # ❌ ESCLUDI NUMERI ULTIMA ESTRAZIONE
        numeri_caldi = [n for n in ordinati if n not in ultima]

        # PRENDI I PRIMI 2
        numeri_caldi = numeri_caldi[:2]

        # SE NON BASTANO
        if len(numeri_caldi) < 2:
            for n in ordinati:
                if n not in numeri_caldi:
                    numeri_caldi.append(n)
                if len(numeri_caldi) == 2:
                    break

        # 🎯 AMBO FORTE
        ambo = f"{numeri_caldi[0]}-{numeri_caldi[1]}"

        # 🔄 CICLOMETRIA BASE
        ciclometria = [
            f"{estrazioni[-1][0]}-{estrazioni[-2][0]}",
            f"{estrazioni[-1][1]}-{estrazioni[-2][1]}"
        ]

        # 📉 SATURAZIONE (media frequenze)
        saturazione = round(sum(freq.values()) / len(freq), 2)

        risultato.append({
            "ruota": ruota,
            "ultima": ultima,
            "numeri_caldi": numeri_caldi,
            "ambo_forte": ambo,
            "ciclometria": ciclometria,
            "saturazione": saturazione
        })

    return risultato