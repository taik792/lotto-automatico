from flask import Flask, jsonify, request
import json
import os
import requests
from base64 import b64encode

app = Flask(__name__)

# ===== CONFIG =====
GITHUB_REPO = "TAIK792/lotto-automatico"
FILE_PATH = "estrazioni.json"
BRANCH = "main"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# ===== FUNZIONE LETTURA FILE LOCALE =====
def carica_dati():
    with open(FILE_PATH, "r") as f:
        return json.load(f)

# ===== FUNZIONE SALVATAGGIO SU GITHUB =====
def salva_su_github(nuovi_dati):

    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Recupera SHA attuale
    r = requests.get(url, headers=headers)
    sha = r.json()["sha"]

    contenuto = json.dumps(nuovi_dati, indent=2)
    encoded_content = b64encode(contenuto.encode()).decode()

    data = {
        "message": "Aggiornamento automatico estrazioni",
        "content": encoded_content,
        "sha": sha,
        "branch": BRANCH
    }

    requests.put(url, headers=headers, json=data)

# ===== ANALISI BASE =====
def analizza_ruota(estrazioni_ruota):
    ultima = estrazioni_ruota[0]

    return {
        "ultima_estrazione": ultima,
        "ambo_prudente": sorted(ultima[:2]),
        "ambo_bilanciato": [min(ultima), max(ultima)],
        "ambo_ritardo": [],
        "terno_strategico": sorted(ultima[:3])
    }

# ===== API PRINCIPALE =====
@app.route("/api")
def api():
    dati = carica_dati()
    risultato = {}

    for ruota, estrazioni in dati.items():
        risultato[ruota] = analizza_ruota(estrazioni)

    return jsonify(risultato)

# ===== AGGIORNA ESTRAZIONE =====
@app.route("/aggiorna", methods=["POST"])
def aggiorna():

    dati = carica_dati()
    payload = request.json

    ruota = payload.get("ruota")
    numeri = payload.get("numeri")

    if ruota not in dati:
        return jsonify({"errore": "Ruota non valida"})

    if len(numeri) != 5:
        return jsonify({"errore": "Servono 5 numeri"})

    dati[ruota].insert(0, numeri)

    salva_su_github(dati)

    return jsonify({"successo": True})

@app.route("/")
def home():
    return "API Lotto attiva"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)











        











