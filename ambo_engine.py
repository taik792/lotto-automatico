def genera_giocata_top(ruote, segnali):
    classifica = []

    for r in ruote:
        score = r["saturazione"]

        # BONUS cross ruote 🔥
        bonus_cross = sum(
            s["forza"] for s in segnali if s["a"] == r["ruota"]
        )

        score += bonus_cross

        classifica.append((score, r))

    top = sorted(classifica, key=lambda x: x[0], reverse=True)[:3]

    return [
        {
            "ruota": r["ruota"],
            "ambo": r["ambo_forte"]
        }
        for _, r in top
    ]