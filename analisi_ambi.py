from collections import Counter
from utils import prendi_ultime_estrazioni

def analizza_ruote(dati):
    risultato = []

    for ruota, estrazioni in dati.items():

        try:
            # 🔥 NORMALIZZA DATI
            estrazioni_pulite = []

            for e in estrazioni:
                if isinstance(e, dict):
                    if "numeri" in e:
                        estrazioni_pulite.append([int(x) for x in e["numeri"]])
                elif isinstance(e, list):
                    estrazioni_pulite.append([int(x) for x in e])

            if len(estrazioni_pulite) < 2:
                continue

            ultime = prendi_ultime_estrazioni(estrazioni_pulite)

            if not ultime:
                continue

            ultima = ultime[-1]

            # 🔥 FREQUENZE
            freq = Counter()
            for estr in ultime:
                freq.update(estr)

            ordinati = sorted(freq, key=freq.get, reverse=True)

            # ❌ ESCLUDI ULTIMA
            numeri_caldi = [n for n in ordinati if n not in ultima]

            if len(numeri_caldi) < 2:
                numeri_caldi = ordinati[:2]

            numeri_caldi = numeri_caldi[:2]

            ambo = f"{numeri_caldi[0]}-{numeri_caldi[1]}"

            # 🔁 CICLOMETRIA FIXATA
            def ritardo(numero):
                count = 0
                trovato = False

                for estr in reversed(ultime):
                    if numero in estr:
                        trovato = True
                        break
                    count += 1

                return count if trovato else len(ultime)

            ciclo1 = ritardo(numeri_caldi[0])
            ciclo2 = ritardo(numeri_caldi[1])

            # 🔥 evita 0
            if ciclo1 == 0: ciclo1 = 1
            if ciclo2 == 0: ciclo2 = 1

            # 📊 SATURAZIONE
            totale = sum(freq.values())
            sat = (freq[numeri_caldi[0]] + freq[numeri_caldi[1]]) / totale if totale > 0 else 0

            risultato.append({
                "ruota": ruota,
                "ultima": ultima,
                "numeri_caldi": numeri_caldi,
                "ambo_forte": ambo,
                "ciclometria": f"{ciclo1} | {ciclo2}",
                "saturazione": round(sat * 10, 2)
            })

        except Exception as e:
            print(f"Errore su {ruota}: {e}")
            continue

    return risultato