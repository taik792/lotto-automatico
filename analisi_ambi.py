from utils import prendi_ultime_estrazioni

def analizza_ruote(dati):
    risultato = []

    for ruota, estrazioni in dati.items():

        # 🔥 PRENDI SOLO LE ULTIME
        ultime = prendi_ultime_estrazioni(estrazioni)

        if len(ultime) < 2:
            continue

        # ✅ ULTIMA ESTRAZIONE
        ultima = ultime[-1]

        # 🔢 FREQUENZE
        freq = {}
        for estr in ultime:
            for n in estr:
                freq[n] = freq.get(n, 0) + 1

        # 🔥 NUMERI CALDI (ordinati)
        ordinati = sorted(freq, key=freq.get, reverse=True)

        # ❌ ESCLUDI NUMERI DELL’ULTIMA
        numeri_caldi = [n for n in ordinati if n not in ultima][:2]

        # 🔁 CICLOMETRIA (ritardo)
        ritardi = {}

        for numero in numeri_caldi:
            ritardo = 0
            for estr