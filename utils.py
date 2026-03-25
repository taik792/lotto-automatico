ULTIME_ESTRAZIONI = 80  # puoi mettere 200–500

def prendi_ultime_estrazioni(lista_estrazioni):
    if not lista_estrazioni:
        return []
    return lista_estrazioni[-ULTIME_ESTRAZIONI:]