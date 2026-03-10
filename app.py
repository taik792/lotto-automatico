import json
import requests
from collections import Counter
from itertools import combinations

# ----------------------------
# SCARICA ULTIME ESTRAZIONI
# ----------------------------

url = "https://raw.githubusercontent.com/MatteoMarchetti/lotto-data/master/lotto_latest.json"

try:
    response = requests.get(url)
    nuove = response.json()
except:
    nuove = None

# ----------------------------
# CARICA STORICO
# ----------------------------

with open("estrazioni.json","r") as f:
    data = json.load(f)

ruote = list(data.keys())

# ----------------------------
# AGGIORNA STORICO
# ----------------------------

if nuove:

    for ruota in ruote:

        nuova = nuove[ruota]

        if data[ruota][0] != nuova:
            data[ruota].insert(0, nuova)

# salva storico aggiornato
with open("estrazioni.json","w") as f:
    json.dump(data,f,indent=2)

# ----------------------------
# PARAMETRI
# ----------------------------

ULTIME_ESTRAZIONI = 24
TOP_NUMERI = 4
NUMERI_FINALI = 2

# ----------------------------
# FREQUENZA
# ----------------------------

def calcola_frequenza(estrazioni):

    freq = Counter()

    for estr in estrazioni[:ULTIME_ESTRAZIONI]:

        for n in estr:

            freq[n]+=1

    return freq

# ----------------------------
# RITARDO
# ----------------------------

def calcola_ritardo(estrazioni):

    ritardi = {}

    for n in range(1,91):

        ritardo=0

        for estr in estrazioni:

            if n in estr:
                break

            ritardo+=1

        ritardi[n]=ritardo

    return ritardi

# ----------------------------
# SCORE NUMERI
# ----------------------------

def score_numeri(freq,ritardi):

    score={}

    for n in range(1,91):

        score[n]=freq.get(n,0)+ritardi.get(n,0)

    return score

# ----------------------------
# ANALISI RUOTE
# ----------------------------

risultati=[]

for ruota in ruote:

    estrazioni=data[ruota]

    freq=calcola_frequenza(estrazioni)

    ritardi=calcola_ritardo(estrazioni)

    score=score_numeri(freq,ritardi)

    top=sorted(score.items(),key=lambda x:x[1],reverse=True)[:TOP_NUMERI]

    top_numeri=[n[0] for n in top]

    migliori_coppie=[]

    for c in combinations(top_numeri,2):

        forza=score[c[0]]+score[c[1]]

        migliori_coppie.append((c,forza))

    migliori_coppie.sort(key=lambda x:x[1],reverse=True)

    risultati.append({

        "ruota":ruota,
        "ultima_estrazione":estrazioni[0],
        "numeri_caldi":top_numeri[:NUMERI_FINALI],
        "ambo_forte":list(migliori_coppie[0][0]),
        "saturazione":round(sum(score.values())/90,2)

    })

# ----------------------------
# ANALISI GLOBALE
# ----------------------------

ruota_top=max(risultati,key=lambda x:x["saturazione"])["ruota"]

ruota_satura=ruota_top

# ----------------------------
# SALVA RISULTATI
# ----------------------------

output={

    "ruote":risultati,

    "ruota_top_settimana":ruota_top,

    "ruota_piu_satura":ruota_satura,

    "ambi_ciclici":[],

    "convergenza_ruote":[]

}

with open("risultati.json","w") as f:

    json.dump(output,f,indent=2)