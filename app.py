from flask import Flask, jsonify
import requests
import os
import base64

app = Flask(__name__)

GITHUB_USER = "taik792"
REPO = "lotto-automatico"
FILE_PATH = "estrazioni.json"

TOKEN = os.getenv("TOKEN")

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia"
]

def carica_dati():
    url = f"https://api.github.com/repos/{GITHUB_USER}/{REPO}/contents/{FILE_PATH}"

    headers = {
        "Authorization": f"token {TOKEN}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    content = base64.b64decode(data["content"]).decode("utf-8")
    return eval(content)


def calcola_ritardi(estrazioni):
    ritardi = {n: 0 for n in range(1,91)}

    for numero in ritardi:
        for i, estrazione in enumerate(estrazioni):
            if numero in estrazione:
                ritardi[numero] = i
                break

    numero_ritardo = max(ritardi, key=ritardi.get)
    return numero_ritardo


def calcola_frequenze(estrazioni, ultime=50):
    conteggio = {n: 0 for n in range(1,91)}
    for estrazione in estrazioni[:ultime]:
        for n in estrazione:
            conteggio[n] += 1

    numero_freq = max(conteggio, key=conteggio.get)
    return numero_freq


def analizza_ruota(estrazioni):
    ultima = estrazioni[0]

    ritardo = calcola_ritardi(estrazioni)
    frequente = calcola_frequenze(estrazioni)

    ambo = sorted([ritardo, frequente])

    terzo = (ritardo + frequente) % 90
    if terzo == 0:
        terzo = 90

    terno = sorted([ritardo, frequente, terzo])

    return {
        "ultima_estrazione": ultima,
        "numero_ritardo": ritardo,
        "numero_frequente": frequente,
        "ambo_strategico": ambo,
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
    return "API Lotto PRO attiva"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)



















        











