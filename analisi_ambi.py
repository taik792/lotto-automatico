from collections import Counter
from utils import prendi_ultime_estrazioni

def analizza_ruote(dati):
    risultato = []

    for ruota, estrazioni in dati.items():

        try:
            # 🔥 NORMALIZZA
            estrazioni_pulite = []

            for e in estrazioni:
                if isinstance(e, dict) and "numeri" in e:
                    estrazioni_pulite.append([int(x) for x in e["numeri"]])
                elif isinstance(e, list):
                    estrazioni_pulite.append([int(x) for x in e])

            if len(estrazioni_pulite) < 20:
                continue

            ultime = prendi_ultime_estrazioni(estrazioni_pulite)
            ultima = ultime[-1]

            # 🔢 FREQUENZE
            freq = Counter()
            for estr in ultime:
                freq.update(estr)

            totale_estrazioni = len(ultime)

            def ritardo(numero):
                count = 0
                for estr in reversed(ultime):
                    if numero in estr:
                        return count
                    count += 1
                return count

            def ciclo_medio(numero):
                presenze = freq[numero]
                if presenze == 0:
                    return totale_estrazioni
                return totale_estrazioni / presenze

            numeri_score = []

            for numero in freq.keys():

                if numero in ultima:
                    continue

                r = ritardo(numero)
                cm = ciclo_medio(numero)

                indice = r / cm if cm > 0 else 0

                # 🔥 PUNTEGGIO
                score = (indice * 2) + (freq[numero] / totale_estrazioni)

                numeri_score.append((numero, score, r, cm, indice))

            # 🔥 ordina per punteggio
            numeri_score.sort(key=lambda x: x[1], reverse=True)

            if len(numeri_score) < 2:
                continue

            n1 = numeri_score[0]
            n2 = numeri_score[1]

            ambo = f"{n1[0]}-{n2[0]}"

            saturazione = round((n1[1] + n2[1]) / 2, 2)

            risultato.append({
                "ruota": ruota,
                "ultima": ultima,
                "numeri_caldi": [n1[0], n2[0]],
                "ambo_forte": ambo,
                "ciclometria": f"{n1[2]} | {n2[2]}",
                "indice": f"{round(n1[4],2)} | {round(n2[4],2)}",
                "saturazione": saturazione
            })

        except Exception as e:
            print(f"Errore {ruota}: {e}")
            continue

    return risultato