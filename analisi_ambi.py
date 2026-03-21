def analizza_ruote(dati):
    risultato = []

    for ruota in dati["ruote"]:
        nome = ruota["ruota"]
        ultima = ruota["ultima"]

        # NUMERI CALDI (primi 2 più frequenti)
        freq = {}
        for n in ultima:
            freq[n] = freq.get(n, 0) + 1

        ordinati = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        numeri_caldi = [x[0] for x in ordinati[:2]]

        # CICLOMETRIA (coppie consecutive)
        ciclometria = []
        for i in range(len(ultima) - 1):
            ciclometria.append(f"{ultima[i]}-{ultima[i+1]}")

        ciclometria = ciclometria[:2]

        # SATURAZIONE
        saturazione = round(sum(ultima) / len(ultima) / 20, 2)

        risultato.append({
            "ruota": nome,
            "ultima": ultima,
            "numeri_caldi": numeri_caldi,
            "ambo_forte": f"{numeri_caldi[0]}-{numeri_caldi[1]}",
            "ciclometria": ciclometria,
            "saturazione": saturazione
        })

    return risultato