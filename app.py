from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# DATI SIMULATI (poi li sistemiamo automatici)
dati = {
    "Bari": [12, 34, 45, 56, 78],
    "Cagliari": [17, 18, 29, 40, 51],
    "Firenze": [3, 14, 25, 36, 47],
    "Genova": [6, 17, 28, 39, 50],
    "Milano": [5, 16, 27, 38, 49],
    "Napoli": [11, 22, 33, 44, 55],
    "Palermo": [2, 13, 24, 35, 46],
    "Roma": [15, 26, 37, 48, 59],
    "Torino": [8, 19, 30, 41, 52],
    "Venezia": [9, 20, 31, 42, 53]
}

@app.route("/api")
def api():
    return jsonify(dati)

@app.route("/")
def home():
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Lotto Live Statistiche</title>
        <style>
            body {
                font-family: Arial;
                background: linear-gradient(to bottom, #004e92, #000428);
                color: white;
                text-align: center;
                padding: 30px;
            }
            .ruota {
                margin: 20px;
                padding: 15px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
            }
            span {
                display: inline-block;
                margin: 5px;
                padding: 10px;
                background: orange;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                line-height: 20px;
                font-weight: bold;
            }
        </style>
    </head>
    <body>
        <h1>🎯 Lotto Live Statistiche</h1>
        <div id="contenitore"></div>

        <script>
            fetch("/api")
            .then(res => res.json())
            .then(data => {
                const cont = document.getElementById("contenitore");

                Object.entries(data).forEach(([ruota, numeri]) => {
                    const div = document.createElement("div");
                    div.className = "ruota";
                    div.innerHTML = "<h2>" + ruota + "</h2>" +
                        numeri.map(n => "<span>"+n+"</span>").join("");
                    cont.appendChild(div);
                });
            })
            .catch(err => {
                document.getElementById("contenitore").innerHTML =
                    "<h2>Errore caricamento dati</h2>";
            });
        </script>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)























        











