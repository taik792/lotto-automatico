from flask import Flask, jsonify, request, g
import sqlite3
import os

app = Flask(__name__)

DATABASE = 'lotto.db'

# ===============================
# DATABASE
# ===============================

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
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
            data_creazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    db.commit()

@app.before_request
def initialize():
    init_db()

# ===============================
# FUNZIONE DURATA DINAMICA AMBO
# ===============================

def calcola_durata_ambo(num1, num2, ruota):
    # QUI DENTRO POI METTI LA TUA FORMULA VERA
    indice = (num1 + num2) % 7 + 2   # placeholder intelligente
    if indice < 2:
        indice = 2
    if indice > 8:
        indice = 8
    return indice

# ===============================
# SALVA GIOCATA
# ===============================

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
        (tipo, num1, num2, ruota, durata_attuale, estrazioni_passate, stato)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, ("ambo", num1, num2, ruota, durata, 0, "attivo"))

    db.commit()

    return jsonify({
        "messaggio": "Ambo salvato",
        "durata_calcolata": durata
    })

# ===============================
# AGGIORNA GIOCATE (SIMULAZIONE)
# ===============================

@app.route("/aggiorna-giocate", methods=["POST"])
def aggiorna_giocate():
    estrazione = request.json   # {"Roma": [12,45,33,10,88]}

    db = get_db()
    giocate = db.execute(
        "SELECT * FROM giocate_attive WHERE stato='attivo'"
    ).fetchall()

    for g in giocate:
        numeri_ruota = estrazione.get(g["ruota"], [])

        # Controllo uscita
        if g["num1"] in numeri_ruota and g["num2"] in numeri_ruota:
            db.execute("""
                UPDATE giocate_attive
                SET stato=?
                WHERE id=?
            """, ("uscito", g["id"]))
            continue

        # Durata dinamica
        nuova_durata = calcola_durata_ambo(g["num1"], g["num2"], g["ruota"])
        nuove_passate = g["estrazioni_passate"] + 1

        stato = "attivo"
        if nuove_passate >= nuova_durata:
            stato = "scaduto"

        db.execute("""
            UPDATE giocate_attive
            SET durata_attuale=?, estrazioni_passate=?, stato=?
            WHERE id=?
        """, (nuova_durata, nuove_passate, stato, g["id"]))

    db.commit()

    return jsonify({"messaggio": "Giocate aggiornate"})

# ===============================
# VEDI GIOCATE ATTIVE
# ===============================

@app.route("/giocate-attive")
def giocate_attive():
    db = get_db()
    giocate = db.execute(
        "SELECT * FROM giocate_attive ORDER BY id DESC"
    ).fetchall()
    return jsonify([dict(g) for g in giocate])

# ===============================
# TEST BASE
# ===============================

@app.route("/")
def home():
    return jsonify({"status": "Backend Lotto Live attivo"})

# ===============================
# AVVIO
# ===============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
