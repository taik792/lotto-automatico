import json
from analisi_ambi import analizza_ruote
from ambo_engine import genera_giocata_top
from analisi_cross import analisi_cross_ruote


def main():
    with open("estrazioni.json", "r") as f:
        dati = json.load(f)

    ruote = analizza_ruote(dati)

    # 🔥 NUOVO
    segnali = analisi_cross_ruote(dati)

    giocate_top = genera_giocata_top(ruote, segnali)

    risultato = {
        "ruote": ruote,
        "giocate_top": giocate_top,
        "segnali_cross": segnali
    }

    with open("risultati.json", "w") as f:
        json.dump(risultato, f, indent=4)


if __name__ == "__main__":
    main()