def analizza_ruote(dati):
    risultato = []

    for ruota, estrazioni in dati.items():

        # Prendi ultime 5 estrazioni
        ultime = estrazioni[-5:]

        # Flatten numeri
        numeri = [n for estrazione in ultime for n in estrazione]

        # Conta frequenze
        freq = {}
        for n in numeri:
            freq[n] = freq.get(n, 0) + 1

        # Numeri caldi (top 2)
        caldi = sorted(freq, key=freq.get, reverse=True)[:2]

        # ❌ ESCLUDI numeri ultima estrazione
        ultima = ultime[-1]
        caldi = [n for n in caldi if n not in ultima]

        # Se pochi → aggiungi altri
        if len(caldi) < 2:
            extra = sorted(freq, key=freq.get, reverse=True)
            for n in extra:
                if n not in caldi and n not in ultima:
                    caldi.append(n)
                if len(caldi) == 2:
                    break

        # Ambo forte
        ambo = f"{caldi[0]}-{caldi[1]}"

        # Ciclometria base
        ciclometria = [
            f"{ultime[-1][0]}-{ultime[-2][0]}",
            f"{ultime[-1][1]}-{ultime[-2][1]}"
        ]

        risultato.append({
            "ruota": ruota,
            "ultima": ultima,
            "numeri_caldi": caldi,
            "ambo_forte": ambo,
            "ciclometria": ciclometria,
            "saturazione": round(sum(freq.values()) / len(freq), 2)
        })

    return risultato