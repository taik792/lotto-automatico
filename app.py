from flask import Flask, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

FILE_ESTRAZIONI = "estrazioni.json"

def carica_dati():
    with open(FILE_ESTRAZIONI, "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def home():
    return "Backend Lotto Statistiche attivo"

@app.route("/api")
def api():
    try:
        estrazioni = carica_dati()

        return jsonify({
            "status": "ok",
            "numero_estrazioni": len(estrazioni),
            "prime_chiavi": list(estrazioni[0].keys()) if len(estrazioni) > 0 else []
        })

    except Exception as e:
        return jsonify({
            "errore": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

























        











