import json
import os
from collections import defaultdict

# ================================
# CONFIG
# ================================
TOP_NUMERI = 12
AMBI_FINALI = 20

PESO_FREQ = 2.0
PESO_SCORE = 1.5
PESO_RITARDO = 0.3


# ================================
# PATH FILE
# ================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

file_estrazioni = os.path.join(BASE_DIR, "estrazioni.json")
file_output = os.path.join(BASE_DIR, "risultati.json")


# ================================
# CARICA ESTRAZIONI
# ================================
with open(file_estrazioni, "r") as f:
    estrazioni = json.load(f)

# ⚠️ IMPORTANTISSIMO → invertiamo (più recenti prima)
estrazioni = estrazioni[::-1]


# ================================
# CALCOLO RITARDI
# ================================
ritardi = {i: 0 for i in range(1