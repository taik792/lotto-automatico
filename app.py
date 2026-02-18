from flask import Flask, jsonify
from flask_cors import CORS
import json
import os
from collections import Counter

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_ESTRAZIONI = os.path.join(BASE_DIR, "estrazioni.json")

FINESTRA_50 = 50
FINESTRA_100 = 100


def carica_dati():
    with open(FILE_ESTRAZIONI, "r", encoding="utf-8") as f:
        return json.load(f)


def analizza_ruota(lista_estrazioni):

    tutte = []
    for estrazione in lista_estrazioni:
        tutte.extend(estrazione)

    ultimi_50 = tutte[-FINESTRA_50:]
    ultimi_100 = tutte[-FINESTRA_100:]

    freq_totale = Counter(tutte)
    freq_50 = Counter(ultimi_50)
    freq_100 = Counter(ultimi_100)

    # Numeri caldi
    caldi = [n for n, _ in freq_50.most_common(5)]

    # Numeri freddi
    freddi = [n for n in range(1, 91) if freq_100[n] == 0][:5]

    # Ritardatario
    ritardi = {}
    for numero in range(1, 91):
        ritardo = 0
        for estrazione in reversed(lista_estrazioni):
            if numero not in estrazione:
                ritardo += 1
            else:
                break
        ritardi[numero] = ritardo

    ritardatario = max(ritardi, key=ritardi.get)

    # Indice pressione
    pressione = {}
    for numero in range(1, 91):
        pressione[numero] = (
            freq_50[numero] * 3 +
            freq_100[numero] * 2 +

























        











