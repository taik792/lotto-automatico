from flask import Flask, jsonify
from flask_cors import CORS
import json
from collections import Counter

app = Flask(__name__)
CORS(app)

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def carica_dati():
    with open("estrazioni.json", "r", encoding="utf-8") as f:
        return json.load(f)

def analizza_ruota(estrazioni_ruota):
    ultime20 = estrazioni_ruota[:20]

    # Frequenze
    frequenze = Counter()
    for estrazione in ultime20:
        frequenze.update(estrazione)

    # Numeri più frequenti
    caldi = [n for n,_ in frequenze.most_common(5)]

    # Ritardi (numeri non usciti nelle 20)
    tutti = set(range(1,91))
    usciti = set(frequenze.keys())
    ritardatari = list(tutti - usciti)
    ritardatari.sort()

    # Ambo Prudente
    ambo_prudente = [caldi[0], caldi[1]] if len(caldi) >= 2 else caldi

    # Ambo Bilanciato
    bassi = [n for n in caldi if n <= 45]
    alti = [n for n in caldi if n > 45]
    if bassi and alti:
        ambo_bilanciato = [bassi[0], alti[0]]
    else:
        ambo_bilanciato = ambo_prudente

    # Ambo Ritardo
    ambo_ritardo = ritardatari[:2] if len(ritardatari) >= 2 else []

    # Terno Strategico
    terno = []
    if caldi:
        terno.append(caldi[0])
    if ritardatari:
        terno.append(ritardatari[0])
    if len(caldi) > 2:
        terno.append(caldi[2])

    return {
        "ultima_estrazione": estrazioni_ruota[0],
        "ambo_prudente": ambo_prudente,
        "ambo_bilanciato": ambo_bilanciato,
        "ambo_ritardo": ambo_ritardo,
        "terno_strategico": terno
    }

@app.route("/api")
def api():
    try:
        dati = carica_dati()
        risultato = {}

        for ruota in RUOTE:
            if ruota in dati:
                risultato[ruota] = analizza_ruota(dati[ruota])

        return jsonify(risultato)

    except Exception as e:
        return jsonify({"errore": str(e)})

@app.route("/")
def home():
    return "API Lotto attiva"

if __name__ == "__main__":
    app.run()








        











