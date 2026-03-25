import json
from analisi_ambi import analizza_ruote

def main():

    with open("estrazioni.json", "r") as f:
        dati = json.load(f)

    ruote = analizza_ruote(dati)

    # 🔥 TOP GIOCATE (le migliori 3)
    top = sorted(ruote, key=lambda x: x["saturazione"], reverse=True)[:3]

    output = {
        "ruote": ruote,
        "giocate_top": [
            {"ruota": r["ruota"], "ambo": r["ambo_forte"]}
            for r in top
        ]
    }

    with open("risultati.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()