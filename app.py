from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # abilita CORS per GitHub Pages

RUOTE = ["Bari", "Cagliari", "Firenze", "Genova", "Milano",
         "Napoli", "Palermo", "Roma", "Torino", "Venezia"]

def carica_dati():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

def analizza_ruota(estrazioni_ruota):
    ultima = estrazioni_ruota[0]

    # esempi logica semplice
    ambo_prudente = ultima[:2]
    ambo_bilanciato = ultima[1:3]
    ambo_ritardo = ultima[3:5]
    terno = ultima[:3]

    return {
        "ultima_estrazione": ultima,
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
    app.run(host="0.0.0.0", port=10000)












        











