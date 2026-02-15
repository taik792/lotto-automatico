import os
from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

with open("estrazioni.json", "r") as f:
    estrazioni = json.load(f)

def calcola_previsioni(numeri):
    ultimi_20 = numeri[-20:]

    frequenze = {}
    for estrazione in ultimi_20:
        for numero in estrazione:
            frequenze[numero] = frequenze.get(numero, 0) + 1

    ordinati = sorted(frequenze.items(), key=lambda x: x[1], reverse=True)
    piu_frequenti = [n[0] for n in ordinati]

    ambo_prudente = piu_frequenti[:2]

    bassi = [n for n in piu_frequenti if n <= 45]
    alti = [n for n in piu_frequenti if n > 45]
    ambo_bilanciato = [bassi[0], alti[0]] if bassi and alti else piu_frequenti[:2]

    usciti = set(num for estrazione in ultimi_20 for num in estrazione)
    tutti = set(range(1, 91))
    ritardatari = list(tutti - usciti)
    ambo_ritardo = ritardatari[:2]

    terno = [ambo_prudente[0], ambo_ritardo[0], ambo_prudente[1]]

    return {
        "ambo_prudente": ambo_prudente,
        "ambo_bilanciato": ambo_bilanciato,
        "ambo_ritardo": ambo_ritardo,
        "terno_strategico": terno
    }

@app.route("/api")
def api():
    risultato = {}
    for ruota, estrazioni_ruota in estrazioni.items():
        previsioni = calcola_previsioni(estrazioni_ruota)
        risultato[ruota] = {
            "ultima_estrazione": estrazioni_ruota[-1],
            **previsioni
        }
    return jsonify(risultato)

@app.route("/")
def home():
    return "API Lotto attiva"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)








        











