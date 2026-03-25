ULTIME_ESTRAZIONI = 300  # puoi mettere anche 500

def prendi_ultime_estrazioni(lista_estrazioni):
    if not lista_estrazioni:
        return []
    return lista_estrazioni[-ULTIME_ESTRAZIONI:]