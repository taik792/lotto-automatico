from flask import Flask, jsonify
from flask_cors import CORS
import requests
from collections import Counter
import os

app = Flask(__name__)
CORS(app)

# -----------------------------
# CONFIGURAZIONE
# -----------------------------

GITHUB_USER = "taik792"
GITHUB_REPO = "lotto-automatico"
FILE_NAME = "estrazioni.json"

TOKEN = os.environ.get("TOKEN")

# -----------------------------
# FUNZIONE PER LEGGERE FILE DA GITHUB
# -----------------------------

def leggi_estrazioni():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{FILE_NAME}"

    headers = {}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"

    response = requests.get(url, headers=headers)
    data = response.json()

    import base64
    contenuto = base64.b64decode(data["content"]).decode("utf-8")

    import json
    return json.loads(contenuto)

# -----------------------------
# ALGORITMO STATISTICO
# -----------------------------

def genera_statistiche(lista_estrazioni):
    numeri = []

    for estrazione in lista_estrazioni:
        numeri.extend(estrazione)

    conteggio = Counter(numeri)

    # Numeri più frequenti
    frequenti = [n for n, _ in conteggio.most_common(10)]

    # Numeri meno frequenti (ritardo statistico)
    meno_frequenti = [n for n, _ in conteggio.most_common()][-10:]

    # Ambo frequenza
    ambo_freq = frequenti[:2]

    # Ambo ritardo
    ambo_rit = meno_frequenti[:2]

    # Ambo bilanciato (1 forte + 1 ritardo)
    ambo_bil = [frequenti[0], meno_frequenti[0]]

    # Terno strategico
    terno = [frequenti[0], frequenti[1], meno_frequenti[0]]

    return ambo_freq, ambo_bil, ambo_rit, terno

# -----------------------------
# API PRINCIPALE
# -----------------------------

@app.route("/")
def home():
    return "API Lotto attiva"

@app.route("/api")
def api_lotto():
    try:
        dati = leggi_estrazioni()
        risultato = {}

        for ruota in dati:
            estrazioni = dati[ruota]

            ultima = estrazioni[-1]

            ambo_freq, ambo_bil, ambo_rit, terno = genera_statistiche(estrazioni)

            risultato[ruota] = {
                "ultima_estrazione": ultima,
                "ambo_prudente": ambo_freq,
                "ambo_bilanciato": ambo_bil,
                "ambo_ritardo": ambo_rit,
                "terno_strategico": terno
            }

        return jsonify(risultato)

    except Exception as e:
        return jsonify({"errore": str(e)})

# -----------------------------
# AVVIO SERVER
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)















        











