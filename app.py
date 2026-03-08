import json
from collections import Counter
from itertools import combinations

ULTIME_ESTRAZIONI = 24
TOP_NUMERI = 4
NUMERI_FINALI = 2

with open("estrazioni.json","r") as f:
    data = json.load(f)

ruote = list(data.keys())

def frequenza(estrazioni):

    freq = Counter()

    for estr in estrazioni[-ULTIME_ESTRAZIONI:]:

        for n in estr:
            freq[n]+=1

    return freq


def ritardi(estrazioni):

    rit = {}

    ultime = estrazioni[-ULTIME_ESTRAZIONI:]

    for n in range(1,91):

        r=0

        for estr in reversed(ultime):

            if n in estr:
                break

            r+=1

        rit[n]=r

    return rit


def score_numeri(freq,rit):

    score={}

    for n in range(1,91):

        score[n]=freq.get(n,0)+rit.get(n,0)

    return score


def convergenza_ruota(estrazioni):

    coppie=Counter()

    for estr in estrazioni[-ULTIME_ESTRAZIONI:]:

        for c in combinations(sorted(estr),2):

            coppie[c]+=1

    return coppie


risultati=[]

tutte_coppie=Counter()

score_ruote={}

for ruota in ruote:

    estrazioni=data[ruota]

    ultima=estrazioni[-1]

    freq=frequenza(estrazioni)

    rit=ritardi(estrazioni)

    score=score_numeri(freq,rit)

    top=sorted(score.items(), key=lambda x:x[1], reverse=True)[:TOP_NUMERI]

    top_numeri=[n[0] for n in top]

    coppie=convergenza_ruota(estrazioni)

    migliori=[]

    for c in combinations(top_numeri,2):

        key=tuple(sorted(c))

        forza=coppie.get(key,0)

        bonus=score[c[0]]+score[c[1]]

        totale=forza*2+bonus

        migliori.append((key,totale))

        tutte_coppie[key]+=totale

    migliori.sort(key=lambda x:x[1],reverse=True)

    score_ruote[ruota]=migliori[0][1]

    risultati.append({

        "ruota":ruota,
        "ultima_estrazione":ultima,
        "numeri_caldi":top_numeri[:NUMERI_FINALI],
        "ambo_forte":migliori[0][0]

    })


# convergenza tra ruote

convergenze=sorted(tutte_coppie.items(), key=lambda x:x[1], reverse=True)[:5]


# ruota più forte

ruota_top=max(score_ruote, key=score_ruote.get)


# ambi ciclici (ritardo alto)

ritardo_ambi=[]

for coppia,val in tutte_coppie.items():

    ritardo_ambi.append((coppia,val))

ritardo_ambi.sort(key=lambda x:x[1], reverse=True)

ambi_ciclici=ritardo_ambi[:5]


output={

    "ruote":risultati,

    "convergenza_ruote":convergenze,

    "ruota_top_settimana":ruota_top,

    "ambi_ciclici":ambi_ciclici

}


with open("risultati.json","w") as f:

    json.dump(output,f,indent=2)


print("Aggiornamento completato")
