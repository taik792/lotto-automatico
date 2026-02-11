from flask import Flask, jsonify
import json
from datetime import datetime

app = Flask(__name__)

FILE = "storico.json"

def genera_dati():
    return {
        "ultimo_aggiornamento": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "Bari": [
            [11,22,33,44,55],
            [5,12,18,34,67],
            [7,14,21,28,35],
            [1,9,19,29,39],
            [3,13,23,33,43],
            [8,18,28,38,48],
            [6,16,26,36,46],
            [10,20,30,40,50],
            [2,12,22,32,42],
            [4,14,24,34,44]
        ]
    }

@app.route("/")
def home():
    with open(FILE, "r") as f:
        dati = json.load(f)
    return jsonify(dati)

@app.route("/aggiorna")
def aggiorna():
    dati = genera_dati()
    with open(FILE, "w") as f:
        json.dump(dati, f, indent=2)
    return {"status": "aggiornato"}
