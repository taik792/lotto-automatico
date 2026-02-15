from flask import Flask, jsonify
from flask_cors import CORS
import json
import random
from collections import Counter

app = Flask(__name__)
CORS(app)

def carica_estrazioni():
    with open("estrazioni.json", "r") as f:
        return json.load(f)

def genera_previsione(numeri):
    # Logica semplice ma sensata:
    # 1. Numeri ritardatari simulati (numeri non presenti)
    # 2. Numeri consecutivi
    # 3. Numeri con stessa decina
    
    tutti = set(range(1, 91))
    usciti = set(numeri)
    
    # Ritardatari (non usciti)
    ritardatari = list(tutti - usciti)
    random.shuffle(ritardatari)
    
    # Prendiamo 3 ritardatari
    previsione = ritardatari[:3]
    
    # Aggiungiamo 2 numeri casuali coerenti
    while len(previsione) < 5:
        n = random.randint(1, 90)
        if n not in previsione:
            previsione.append(n)
    
    return sorted(previsione)

@app.route("/")
def home():
    return "API Lotto attiva"

@app.route("/api")
def api():
    try:
        dati = carica_estrazioni()
        risultato = {}
        
        for ruota, numeri in dati.items():
            risultato[ruota] = {
                "ultima_estrazione": numeri,
                "previsione": genera_previsione(numeri)
            }
        
        return jsonify(risultato)
    
    except Exception as e:
        return jsonify({"errore": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)










