import json

ordine_ruote = [
"Bari",
"Cagliari",
"Firenze",
"Genova",
"Milano",
"Napoli",
"Palermo",
"Roma",
"Torino",
"Venezia"
]

with open("estrazioni.json") as f:
    estrazioni = json.load(f)

risultati = []

for ruota in ordine_ruote:

    dati = estrazioni[ruota]

    ultima = dati[-1]

    ultime = dati[-30:]

    freq = {}

    for estr in ultime:
        for n in estr:
            freq[n] = freq.get(n,0)+1

    ordinati = sorted(freq.items(), key=lambda x:x[1], reverse=True)

    numeri_caldi = [ordinati[0][0], ordinati[1][0]]

    ambo_forte = f"{numeri_caldi[0]}-{numeri_caldi[1]}"

    saturazione = round(sum(freq.values())/len(freq),2)

    # -------------------
    # CICLOMETRIA
    # -------------------

    a = ultima[0]
    b = ultima[1]

    d = abs(a-b)
    d2 = 90-d

    c1 = (b + d) % 90
    c2 = (b + d2) % 90

    c3 = (a + d) % 90
    c4 = (a + d2) % 90

    ciclometrici = []

    for x,y in [(a,b),(b,c1),(b,c2),(a,c3),(a,c4)]:

        if x==0: x=90
        if y==0: y=90

        ciclometrici.append(f"{x}-{y}")

    risultati.append({
        "ruota":ruota,
        "ultima":ultima,
        "numeri_caldi":numeri_caldi,
        "ambo_forte":ambo_forte,
        "ciclometria":ciclometrici,
        "saturazione":saturazione
    })

with open("risultati.json","w") as f:
    json.dump(risultati,f,indent=4)