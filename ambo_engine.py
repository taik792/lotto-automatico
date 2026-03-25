def genera_giocata_top(ruote):
    classifica = []

    for r in ruote:
        try:
            score = r["saturazione"]
            classifica.append((score, r))
        except:
            continue

    top = sorted(classifica, key=lambda x: x[0], reverse=True)[:3]

    risultato = []

    for _, r in top:
        risultato.append({
            "ruota": r["ruota"],
            "ambo": r["ambo_forte"]
        })

    return risultato