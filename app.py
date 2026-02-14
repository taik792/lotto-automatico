from flask import Flask, jsonify, render_template_string
import requests
import re

app = Flask(__name__)

RUOTE = [
    "Bari","Cagliari","Firenze","Genova","Milano",
    "Napoli","Palermo","Roma","Torino","Venezia","Nazionale"
]

def scarica_estrazioni():
    url = "https://www.superenalotto.it/risultati/lotto"
    r = requests.get(url, timeout=10)
    html = r.text

    risultati = {}
    for ruota in RUOTE:
        pattern = rf"{ruota}.*?(\d{{1,2}}).*?(\d{{1,2}}).*?(\d{{1,2}}).*?(\d{{1,2}}).*?(\d{{1,2}})"
        match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
        if match:
            risultati[ruota] = [int(n) for n in match.groups()]
        else:
            risultati[ruota] = []

    return risultati

@app.route("/api/estrazioni")
def api():
    return jsonify(scarica_estrazioni())

@app.route("/")
def home():
    html = """
    <html>
    <head>
        <title>Lotto Live</title>
        <style>
            body{background:#0f172a;color:white;font-family:Arial;padding:20px}
            .card{background:#1e293b;padding:15px;margin:10px 0;border-radius:10px}
        </style>
    </head>
    <body>
    <h1>📊 Lotto Live</h1>
    <div id="contenuto">Caricamento...</div>

    <script>
    fetch('/api/estrazioni')
        .then(r => r.json())
        .then(data => {
            let html = '';
            for (let ruota in data){
                html += `<div class="card"><h2>${ruota}</h2>${data[ruota].join(", ")}</div>`;
            }
            document.getElementById("contenuto").innerHTML = html;
        })
        .catch(() => {
            document.getElementById("contenuto").innerHTML = "Errore caricamento dati.";
        });
    </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)


