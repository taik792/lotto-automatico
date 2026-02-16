from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# DATI DEMO (poi li collegheremo al tuo algoritmo)
DATI = {
    "Bari": {
        "ultima_estrazione": [12, 34, 46, 68, 78],
        "ambo_strategico": [12, 34],
        "numero_frequente": [46],
        "numero_ritardo": [78],
        "terno_strategico": [12, 34, 46]
    },
    "Cagliari": {
        "ultima_estrazione": [17, 18, 29, 40, 61],
        "ambo_strategico": [17, 29],
        "numero_frequente": [40],
        "numero_ritardo": [61],
        "terno_strategico": [17, 29, 40]
    },
    "Firenze": {
        "ultima_estrazione": [3, 14, 25, 36, 47],
        "ambo_strategico": [14, 36],
        "numero_frequente": [25],
        "numero_ritardo": [47],
        "terno_strategico": [14, 25, 36]
    },
    "Genova": {
        "ultima_estrazione": [8, 17, 28, 39, 50],
        "ambo_strategico": [17, 28],
        "numero_frequente": [39],
        "numero_ritardo": [50],
        "terno_strategico": [17, 28, 39]
    }
}

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Lotto Live Statistiche</title>
<style>
body {
    margin:0;
    font-family: Arial;
    background: linear-gradient(to bottom, #0f4c75, #3282b8);
    color:white;
}
h1 {
    text-align:center;
    padding:20px;
}
.container {
    width:90%;
    margin:auto;
}
.blocco {
    background: rgba(0,0,0,0.3);
    padding:20px;
    margin:20px 0;
    border-radius:10px;
}
.numero {
    display:inline-block;
    background:#ffcc00;
    color:black;
    padding:10px 15px;
    margin:5px;
    border-radius:50%;
    font-weight:bold;
}
.titolo {
    font-size:20px;
    margin-bottom:10px;
}
</style>
</head>
<body>

<h1>🎯 Lotto Live Statistiche</h1>
<div class="container" id="contenitore"></div>

<script>
fetch("/api")
.then(r => r.json())
.then(data => {

    const contenitore = document.getElementById("contenitore");

    Object.entries(data).forEach(([ruota, valori]) => {

        const blocco = document.createElement("div");
        blocco.className = "blocco";

        blocco.innerHTML = `
            <div class="titolo">${ruota}</div>

            <p><strong>Ultima estrazione:</strong></p>
            ${valori.ultima_estrazione.map(n => `<span class="numero">${n}</span>`).join("")}

            <p><strong>Modalità Prudente (Ambo strategico):</strong></p>
            ${valori.ambo_strategico.map(n => `<span class="numero">${n}</span>`).join("")}

            <p><strong>Numero Frequente:</strong></p>
            ${valori.numero_frequente.map(n => `<span class="numero">${n}</span>`).join("")}

            <p><strong>Numero Ritardo:</strong></p>
            ${valori.numero_ritardo.map(n => `<span class="numero">${n}</span>`).join("")}

            <p><strong>Modalità Aggressiva (Terno strategico):</strong></p>
            ${valori.terno_strategico.map(n => `<span class="numero">${n}</span>`).join("")}
        `;

        contenitore.appendChild(blocco);
    });

});
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/api")
def api():
    return jsonify(DATI)

if __name__ == "__main__":
    app.run()
























        











