from flask import Flask, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# === HOME PAGE ===
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# === API DATI LOTTO ===
@app.route("/api")
def api():
    try:
        with open("storico.json", "r") as f:
            dati = json.load(f)
        return jsonify(dati)
    except:
        return jsonify({"errore": "storico.json non trovato"})

# === AVVIO SERVER ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




