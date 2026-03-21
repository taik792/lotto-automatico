import random

RUOTE_COLLEGATE = {
    "Bari": ["Bari", "Napoli", "Palermo"],
    "Cagliari": ["Cagliari", "Roma", "Firenze"],
    "Firenze": ["Firenze", "Genova", "Roma"],
    "Genova": ["Genova", "Milano", "Torino"],
    "Milano": ["Milano", "Genova", "Venezia"],
    "Napoli": ["Napoli", "Bari", "Palermo"],
    "Palermo": ["Palermo", "Napoli", "Bari"],
    "Roma": ["Roma", "Firenze", "Cagliari"],
    "Torino": ["Torino", "Genova", "Milano"],
    "Venezia": ["Venezia", "Milano", "Torino"]
}

def genera_ambo(numeri_caldi):
    if len(numeri_caldi) < 2:
        return None
    return f"{numeri_caldi[0]}-{numeri_caldi[1]}"

def calcola_score(ruota):
    base = len(ruota["numeri_caldi"]) * 2
    ciclo = len(ruota["ciclometria"])
    sat = max(0, 3 - ruota["saturazione"])
    return round(base + ciclo + sat, 2)

def genera_giocate(dati_ruote):
    giocate = []

    for r in dati_ruote:
        ambo = genera_ambo(r["numeri_caldi"])
        score = calcola_score(r)

        ruote_gioco = RUOTE_COLLEGATE.get(r["ruota"], [r["ruota"]])

        giocate.append({
            "ruota": r["ruota"],
            "ambo": ambo,
            "ruote_gioco": ruote_gioco,
            "score": score,
            "colpi": 3
        })

    giocate = sorted(giocate, key=lambda x: x["score"], reverse=True)

    return giocate[:3]