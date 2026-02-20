from flask import Flask, jsonify, request, g
from flask_cors import CORS
import json
import os
import sqlite3
from collections import Counter

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_ESTRAZIONI = os.path.join(BASE_DIR, "estrazioni.json")
DATABASE = os.path.join(BASE_DIR, "lotto.db")

FINESTRA_50 = 50
FINESTRA_100 = 100

# ==================================================
# DATABASE
# ==================================================

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS giocate_attive (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            num1 INTEGER,
            num2 INTEGER,
            ruota TEXT,
            durata_attuale INTEGER,
            estrazioni_passate INTEGER,
            stato TEXT,
            ultima_estrazione_usata TEXT,
            data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()

@app.before_request
def initialize():
    init_db()

# ==================================================
# FUNZIONE DURATA DINAMICA
# ==================================================

def calcola_durata_ambo(num1, num2, ruota):
    durata = ((num1 + num2) % 6) + 2
    return max(2, min(durata, 8))

# ==================================================
# AGGIORNAMENTO AUTOMATICO
# ==================================================

def aggiorna_giocate_con_estrazioni(dati):

    db = get_db()
    giocate = db.execute(
        "SELECT * FROM giocate_attive WHERE stato='attivo'"
    ).fetchall()

    for g in giocate:

        ruota = g["ruota"]
        if ruota not in dati:
            continue

        ultima_estrazione = dati[ruota][-1]
        ultima_str = ",".join(map(str, ultima_estrazione))

        # Evita aggiornamenti multipli sulla stessa estrazione
        if g["ultima_estrazione_usata"] == ultima_str:
            continue

        # Controllo uscita
        if g["num1"] in ultima_estrazione and g["num2"] in ultima_estrazione:
            db.execute("""
                UPDATE giocate_attive
                SET stato=?, ultima_estrazione_usata=?
                WHERE id=?
            """, ("uscito", ultima_str, g["id"]))
            continue

        nuove_passate = g["estrazioni_passate"] + 1
        nuova_durata = calcola_durata_ambo(g["num1"], g["num2"], ruota)

        stato = "attivo"
        if nuove_passate >= nuova_durata:
            stato = "scaduto"

        db.execute("""
            UPDATE giocate_attive
            SET durata_attuale=?, estrazioni_passate=?, stato=?, ultima_estrazione_usata=?
            WHERE id=?
        """, (nuova_durata, nuove_passate, stato, ultima_str, g["id"]))

    db.commit()

# ==================================================
# DATI LOTTO
# ==================================================

def carica_dati():
    with open(FILE_ESTRAZIONI, "r", encoding="utf-8") as f:
        return json.load(f)

def analizza_ruota(lista_estrazioni):

    tutte = []
    for estrazione in lista_estrazioni:
        tutte.extend(estrazione)

    ultimi_50 = tutte[-FINESTRA_50:]
    ultimi_100 = tutte[-FINESTRA_100:]

    freq_50 = Counter(ultimi_50)
    freq_100 = Counter(ultimi_100)

    caldi = [n for n, _ in freq_50.most_common(5)]
    freddi = [n for n, _ in freq_50.most_common()[:-6:-1]]

    ritardi = {}
    for numero in range(1, 91):
        ritardo = 0
        for estrazione in reversed(lista_estrazioni):
            if numero in estrazione:
                break
            ritardo += 1
        ritardi[numero] = ritardo

    ritardatario = max(ritardi, key=ritardi.get)
    suggeriti = list(set(caldi[:2] + [ritardatario]))[:3]

    ambi = []
    for caldo in caldi[:3]:
        ambi.append((caldo, ritardatario))

    indice_pressione = sum(freq_50.values()) + sum(freq_100.values()) + ritardi[ritardatario]
    ultima_estrazione = lista_estrazioni[-1] if lista_estrazioni else []

    return {
        "caldi": caldi,
        "freddi": freddi,
        "ritardatario": ritardatario,
        "da_giocare": suggeriti,
        "ambi_forti": ambi,
        "indice_pressione": indice_pressione,
        "ultima_estrazione": ultima_estrazione
    }

# ==================================================
# API PRINCIPALE
# ==================================================

@app.route("/api")
def api():

    dati = carica_dati()

    aggiorna_giocate_con_estrazioni(dati)

    risultato = {}
    pressione_massima = 0
    ruota_forte = ""

    for ruota, estrazioni in dati.items():

        stats = analizza_ruota(estrazioni)
        risultato[ruota] = stats

        if stats["indice_pressione"] > pressione_massima:
            pressione_massima = stats["indice_pressione"]
            ruota_forte = ruota

    risultato["ruota_forte"] = ruota_forte

    return jsonify(risultato)

# ==================================================
# SALVA AMBO
# ==================================================

@app.route("/salva-ambo", methods=["POST"])
def salva_ambo():

    data = request.json
    num1 = data["num1"]
    num2 = data["num2"]
    ruota = data["ruota"]

    durata = calcola_durata_ambo(num1, num2, ruota)

    db = get_db()

    db.execute("""
        INSERT INTO giocate_attive 
        (tipo, num1, num2, ruota, durata_attuale, estrazioni_passate, stato, ultima_estrazione_usata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, ("ambo", num1, num2, ruota, durata, 0, "attivo", ""))

    db.commit()

    return jsonify({
        "messaggio": "Ambo salvato",
        "durata_calcolata": durata
    })

# ==================================================
# VEDI GIOCATE
# ==================================================

@app.route("/giocate-attive")
def giocate_attive():
    db = get_db()
    giocate = db.execute(
        "SELECT * FROM giocate_attive ORDER BY id DESC"
    ).fetchall()
    return jsonify([dict(g) for g in giocate])

# ==================================================

@app.route("/")
def home():
    return "Backend Lotto Live attivo"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
