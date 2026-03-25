import json
from analisi_ambi import analizza_ruote
from ambo_engine import genera_giocata_top

def main():
    with open("estrazioni.json") as f:
        dati = json.load(f)

    ruote = analizza_ruote(dati)
    top = genera_giocata_top(ruote)

    output = {
        "ruote": ruote,
        "giocate_top": top
    }

    with open("risultati.json", "w") as f:
        json.dump(output, f, indent=4)


if __name__ == "__main__":
    main()