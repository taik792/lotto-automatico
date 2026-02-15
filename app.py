from flask import Flask, jsonify
import requests
import csv
from io import StringIO
from collections import Counter

app = Flask(__name__)

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

CSV_URL = "https://raw.githubusercontent.com/matteocontrini/lotto-data/master/lotto.csv"

def scarica_dati():
    r = requests.get(CSV_URL)
    r.raise_for_status()
    return r.text

def elabora_dati():
    testo = scarica_dati()
    f = StringIO(testo)
    reader = list(csv.reader(f, delimiter=";"))

    header = reader[0]
    righe = reader[-10:]  # ultimi 10 concorsi

    risultato = {}

    for ruota in RUOTE:
        idx = header.index(ruota)

        numeri_ruota = []

        for riga in righe:
            estratti = riga[idx].split(",")
            numeri_ruota.extend([int(x) for x in estratti])

        freq = Counter(numeri_ruota)
        piu_frequenti = [n for n, _ in freq.most_common(3)]

        tutti = set(range(1, 91))
        usciti = set(numeri_ruota)
        ritardatari = list(tutti - usciti)[:2]

        previsione = piu_frequenti + ritardatari

        ultima = [int(x) for x in righe[-1][idx].split(",")]

        risultato[ruota] = {
            "ultima_estrazione": ultima,
            "previsione": previsione
        }

    return risultato

@app.route("/api")
def api():
    try:
        dati = elabora_dati()
        return jsonify(dati)
    except Exception as e:
        return jsonify({"errore": str(e)})

@app.route("/")
def home():
    return "API Lotto attiva"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)









