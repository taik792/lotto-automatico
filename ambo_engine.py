def genera_giocata_top(ruote):
    classifica = []

    for r in ruote:
        score = r["saturazione"]

        ultima = r["ultima"]
        caldi = r["numeri_caldi"]

        # Bonus numeri NON usciti
        bonus = sum(1 for n in caldi if n not in ultima)
        score += bonus * 0.5

        classifica.append((score, r))

    # 🔥 FIX ORDINAMENTO
    top = sorted(classifica, key=lambda x: x[0], reverse=True)[:3]

    # 🔥 FORMATO GIUSTO PER IL SITO
    return [
        {
            "ruota": r["ruota"],
            "ambo": r["ambo_forte"]
        }
        for _, r in top
    ]