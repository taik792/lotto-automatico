def genera_giocata_top(ruote):
    classifica = []

    # =========================
    # FREQUENZA NUMERI (cross ruote)
    # =========================
    tutti_numeri = []

    for r in ruote:
        try:
            tutti_numeri.extend(r["ambo_forte"])
        except:
            continue

    frequenza = {}
    for n in tutti_numeri:
        frequenza[n] = frequenza.get(n, 0) + 1

    # =========================
    # CALCOLO SCORE
    # =========================
    for r in ruote:
        try:
            n1, n2 = r["ambo_forte"]

            indice1, indice2 = r["indice"]
            ciclo1, ciclo2 = r["ciclo"]
            saturazione = r["saturazione"]

            # =========================
            # BASE SCORE
            # =========================
            score = (
                ((indice1 + indice2) / 2) * 0.4 +
                ((ciclo1 + ciclo2) / 2) * 0.2 +
                (saturazione) * 0.1
            )

            # =========================
            # BONUS RIPETIZIONE
            # =========================
            if frequenza.get(n1, 0) > 1:
                score += 0.5
            if frequenza.get(n2, 0) > 1:
                score += 0.5

            # =========================
            # MIGLIORAMENTO ACCOPPIAMENTO
            # =========================
            distanza = abs(n1 - n2)

            # Penalità numeri troppo vicini
            if distanza < 5:
                score -= 0.5

            # Bonus distanza buona
            if 10 < distanza < 60:
                score += 0.5

            # Bonus pari/dispari
            if (n1 % 2) != (n2 % 2):
                score += 0.3

            # =========================
            # FILTRO ANTI-SPAZZATURA
            # =========================

            # indice troppo basso
            if ((indice1 + indice2) / 2) < 3.5:
                continue

            # ciclo troppo sbilanciato
            if abs(ciclo1 - ciclo2) > 1.5:
                continue

            # =========================
            # AGGIUNTA CLASSIFICA
            # =========================
            classifica.append((score, r))

        except:
            continue

    # =========================
    # ORDINAMENTO TOP PICK
    # =========================
    top = sorted(classifica, key=lambda x: x[0], reverse=True)[:3]

    risultato = []

    for score, r in top:
        risultato.append({
            "ruota": r["ruota"],
            "ambo": r["ambo_forte"],
            "score": round(score, 2)
        })

    return risultato