def analizza_ruote(dati):
    risultato = []

    # 🔥 FIX: supporta sia {"ruote": [...]} che lista diretta
    if isinstance(dati, dict):
        lista_ruote = dati.get("ruote", [])
    else:
        lista_ruote = dati

    for ruota in lista_ruote:
        nome = ruota["ruota"]
        ultima = ruota["ultima"]

        # NUMERI CALDI
        freq = {}
        for n in ultima:
            freq[n] = freq.get(n, 0) + 1

        ordinati = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        numeri_caldi = [x[0] for x in ordinati[:2]]

        # CICLOMETRIA
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