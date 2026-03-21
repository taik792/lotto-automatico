import json
from analisi_ambi import analizza_ruote
from ambo_engine import genera_giocata_top


def main():
    with open("estrazioni.json", "r") as f:
        dati = json.load(f)

    ruote = analizza_ruote(dati)

    giocate_top = genera_giocata_top(ruote)

    risultato = {
        "ruote": ruote,
        "giocate_top": giocate_top
    }

    with open("risultati.json", "w") as f:
        json.dump(risultato, f, indent=4)


if __name__ == "__main__":
    main()