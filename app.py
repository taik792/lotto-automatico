from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)  # 👈 QUESTA RIGA È FONDAMENTALE

@app.route("/")
def home():
    return "API Lotto attiva"

@app.route("/api")
def api():

    with open("estrazioni.json", "r", encoding="utf-8") as f:
        archivio = json.load(f)

    risultato = []
    ruota_forte = None
    punteggio_max = 0

    for ruota, estrazioni in archivio.items():

        ultime_50 = estrazioni[-50:]
        conteggio = {}

        for estrazione in ultime_50:
            for numero in estrazione:
                conteggio[numero] = conteggio.get(numero, 0) + 1

        numeri_caldi = sorted(conteggio, key=conteggio.get, reverse=True)[:3]
        indice_pressione = sum(conteggio[n] for n in numeri_caldi)

        if indice_pressione > punteggio_max:
            punteggio_max = indice_pressione
            ruota_forte = ruota

        risultato.append({
            "ruota": ruota,
            "ultima_estrazione": estrazioni[-1],
            "numeri_caldi": numeri_caldi,
            "indice_pressione": indice_pressione
        })

    return jsonify({
        "dati": risultato,
        "ruota_piu_forte": ruota_forte
    })

if __name__ == "__main__":
    app.run()


























        











