import json
from analisi_ambi import analizza_ruote
from ambo_engine import genera_giocate

def main():
    with open("estrazioni.json") as f:
        dati = json.load(f)

    ruote = analizza_ruote(dati)

    giocate = genera_giocate(ruote)

    output = {
        "ruote": ruote,
        "giocate_top": giocate
    }

    with open("risultati.json", "w") as f:
        json.dump(output, f, indent=4)

if __name__ == "__main__":
    main()