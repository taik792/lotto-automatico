def analizza_ruote(dati):
    risultato = []

    for ruota, estrazioni in dati.items():

        ultime = estrazioni[-5:]
        ultima = ultime[-1]

        # Flatten numeri
        numeri = [n for estrazione in ultime for n in estrazione]

        # Frequenze
        freq = {}
        for n in numeri:
            freq[n] = freq.get(n, 0) + 1

        # Numeri caldi
        caldi = sorted(freq, key=freq.get, reverse=True)

        # ❌ Escludi ultima estrazione
        caldi = [n for n in caldi if n not in ultima]

        # Prendi i primi 2
        caldi = caldi[:2]

        # Se non bastano
        if len(caldi) < 2:
            for n in freq:
                if n not in caldi and n not in ultima:
                    caldi.append(n)
                if len(caldi) == 2:
                    break

        # Ambo
        ambo = f"{caldi[0]}-{caldi[1]}"

        # Ciclometria
        ciclometria = [
            f"{ultima[0]}-{ultime[-2][0]}",
            f"{ultima[1]}-{ultime[-2][1]}"
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