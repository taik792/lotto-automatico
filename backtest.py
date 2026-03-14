import json

# carica storico
with open("estrazioni.json") as f:
    estrazioni = json.load(f)

ruote = list(estrazioni.keys())

test_estrazioni = 100

presenze = 0
ambi = 0
test_totali = 0

for ruota in ruote:

    dati = estrazioni[ruota]

    for i in range(30, min(len(dati)-1, test_estrazioni)):

        storico = dati[:i]
        target = dati[i]

        freq = {}

        ultime = storico[-30:]

        for estr in ultime:
            for n in estr:
                freq[n] = freq.get(n,0)+1

        ordinati = sorted(freq.items(), key=lambda x:x[1], reverse=True)

        numeri_caldi = [ordinati[0][0], ordinati[1][0]]

        # verifica presenza
        if numeri_caldi[0] in target or numeri_caldi[1] in target:
            presenze += 1

        # verifica ambo
        if numeri_caldi[0] in target and numeri_caldi[1] in target:
            ambi += 1

        test_totali += 1

print("TEST COMPLETATO")
print("----------------")

print("Test effettuati:", test_totali)
print("Presenze numeri:", presenze)
print("Ambi presi:", ambi)

if test_totali > 0:

    p_presenze = round((presenze/test_totali)*100,2)
    p_ambi = round((ambi/test_totali)*100,2)

    print("Percentuale presenze:", p_presenze,"%")
    print("Percentuale ambi:", p_ambi,"%")