from flask import Flask, jsonify
from flask_cors import CORS
import json
from collections import Counter

app = Flask(__name__)
CORS(app)

def carica_dati():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

def analizza_ruota(storico):
    numeri_flat = [n for estr in storico for n in estr]
    freq = Counter(numeri_flat)

    # Numeri più frequenti
    frequenti = [n for n, _ in freq.most_common(5)]

    # Ritardatari (non presenti negli ultimi 20)
    tutti = set(range(1, 91))
    usciti = set(numeri_flat)
    ritardatari = list(tutti - usciti)

    # Ultima estrazione
    ultima = storico[-1]

    # Ambo prudente (2 più frequenti)
    ambo_prudente = sorted(frequenti[:2])

    # Ambo bilanciato (1 frequente + 1 ritardatario)
    ambo_bilanciato = sorted([frequenti[0], ritardatari[0]]) if ritardatari else ambo_prudente

    # Ambo ritardo (2 ritardatari)
    ambo_ritardo = sorted(ritardatari[:2]) if len(ritardatari) >= 2 else ambo_prudente

    return {
        "ultima_estrazione": ultima,
        "ambo_prudente": ambo_prudente,
        "ambo_bilanciato": ambo_bilanciato,
        "ambo_ritardo": ambo_ritardo
    }

@app.route("/")
def home():
    return "API Lotto attiva"

@app.route("/api")
def api():
    dati = carica_dati()
    risultato = {}

    for ruota, storico in dati.items():
        risultato[ruota] = analizza_ruota(storico)

    return jsonify(risultato)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


        











