from flask import Flask, jsonify
from flask_cors import CORS
import json
from collections import Counter
import os

app = Flask(__name__)
CORS(app)

# ===== FUNZIONI =====

def calcola_statistiche(dati_ruota):
    tutte_estrazioni = []
    for estrazione in dati_ruota:
        tutte_estrazioni.extend(estrazione)

    conteggio = Counter(tutte_estrazioni)

    numeri_caldi = [num for num, _ in conteggio.most_common(3)]

    tutti_numeri = set(range(1, 91))
    numeri_presenti = set(tutte_estrazioni)
    numeri_assenti = list(tutti_numeri - numeri_presenti)
    numeri_freddi = numeri_assenti[:3]

    ritardi = {}
    for numero in tutti_numeri:
        ritardo = 0
        for estrazione in reversed(dati_ruota):
            if numero in estrazione:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    ritardo_massimo = max(ritardi.values())

    indice_pressione = round((ritardo_massimo / len(dati_ruota)) * 100, 2) if len(dati_ruota) > 0 else 0

    combinazioni = []
    for i in range(3):
        combinazione = numeri_caldi + numeri_freddi
        combinazioni.append(sorted(combinazione)[:5])

    return numeri_caldi, numeri_freddi, ritardo_massimo, indice_pressione, combinazioni

# ===== API =====

@app.route("/api")
def api():

    try:
        with open("estrazioni.json", "r") as file:
            dati = json.load(file)

        risultato = []

        for ruota, estrazioni in dati.items():

            numeri_caldi, numeri_freddi, ritardo_massimo, indice_pressione, combinazioni = calcola_statistiche(estrazioni)

            risultato.append({
                "ruota": ruota,
                "ultima_estrazione": estrazioni[-1] if len(estrazioni) > 0 else [],
                "numeri_caldi": numeri_caldi,
                "numeri_freddi": numeri_freddi,
                "ritardo_massimo": ritardo_massimo,
                "indice_pressione": indice_pressione,
                "combinazioni_suggerite": combinazioni
            })

        return jsonify({"ruote": risultato})

    except Exception as e:
        return jsonify({"errore": str(e)})

# ===== AVVIO =====

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
























        











