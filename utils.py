ULTIME_ESTRAZIONI = 50  # puoi mettere 200–500

def prendi_ultime_estrazioni(lista_estrazioni):
    if not lista_estrazioni:
        return []
    return lista_estrazioni[-ULTIME_ESTRAZIONI:]