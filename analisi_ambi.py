def analizza_ruote(dati):
    risultato = []

    for nome_ruota, estrazioni in dati.items():

        if not estrazioni:
            continue

        ultima = estrazioni[0]  # 🔥 ultima estrazione

        # NUMERI CALDI (su più estrazioni)
        freq = {}
        for estrazione in estrazioni[:5]:  # ultime 5
            for n in estrazione:
                freq[n] = freq.get(n, 0) + 1

        ordinati = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        numeri_caldi = [x[0] for x in ordinati[:2]]

        # CICLOMETRIA sulla ultima
        ciclometria = []
        for i in range(len(ultima) - 1):
            ciclometria.append(f"{ultima[i]}-{ultima[i+1]}")

        ciclometria = ciclometria[:2]

        # SATURAZIONE
        saturazione = round(sum(ultima) / len(ultima) / 20, 2)

        risultato.append({
            "ruota": nome_ruota,
            "ultima": ultima,
            "numeri_caldi": numeri_caldi,
            "ambo_forte": f"{numeri_caldi[0]}-{numeri_caldi[1]}",
            "ciclometria": ciclometria,
            "saturazione": saturazione
        })

    return risultato