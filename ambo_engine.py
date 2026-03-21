import json
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

def calcola_score(numeri_caldi, ciclometria, saturazione):
    base = len(numeri_caldi) * 2
    ciclo = len(ciclometria)
    sat = max(0, 3 - saturazione)
    return round(base + ciclo + sat, 2)

def genera_ambo(numeri):
    if len(numeri) < 2:
        return None
    return f"{numeri[0]}-{numeri[1]}"

def genera_giocate(dati):
    giocate = []

    for ruota in dati:
        nome = ruota["ruota"]
        numeri_caldi = ruota["numeri_caldi"]
        ciclometria = ruota["ciclometria"]
        saturazione = ruota["saturazione"]

        ambo = genera_ambo(numeri_caldi)
        score = calcola_score(numeri_caldi, ciclometria, saturazione)

        ruote_target = RUOTE_COLLEGATE.get(nome, [nome])

        giocate.append({
            "ruota_origine": nome,
            "ruote_gioco": ruote_target,
            "ambo": ambo,
            "score": score
        })

    # Ordina per score
    giocate = sorted(giocate, key=lambda x: x["score"], reverse=True)

    # Prendi top 3
    return giocate[:3]