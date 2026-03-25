import json
from analisi_ambi import analizza_ruote

def main():
    with open("estrazioni.json") as f:
        dati = json.load(f)

    ruote, top = analizza_ruote(dati)

    output = {
        "ruote": ruote,
        "giocate_top": top
    }

    with open("risultati.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()