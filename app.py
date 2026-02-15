from flask import Flask, jsonify
import requests
import base64
import json

app = Flask(__name__)

# CONFIGURAZIONE REPOSITORY
GITHUB_USER = "taik792"
GITHUB_REPO = "lotto-automatico"
FILE_NAME = "estrazioni.json"


def leggi_estrazioni():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/contents/{FILE_NAME}"

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Errore GitHub: {response.text}")

    data = response.json()

    if "content" not in data:
        raise Exception(f"Risposta GitHub non valida: {data}")

    contenuto = base64.b64decode(data["content"]).decode("utf-8")

    return json.loads(contenuto)


def analizza_ruota(numeri):
    return {
        "ultima_estrazione": numeri,
        "ambo_prudente": numeri[:2],
        "ambo_bilanciato": numeri[1:3],
        "ambo_ritardo": numeri[-2:],
        "terno_strategico": numeri[:3]
    }


@app.route("/api")
def api():
    try:
        estrazioni = leggi_estrazioni()
        risultato = {}

        for ruota, numeri in estrazioni.items():
            risultato[ruota] = analizza_ruota(numeri)

        return jsonify(risultato)

    except Exception as e:
        return jsonify({"errore": str(e)})


@app.route("/")
def home():
    return "API Lotto attiva"


if __name__ == "__main__":
    app.run()

















        











