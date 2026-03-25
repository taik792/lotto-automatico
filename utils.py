ULTIME_ESTRAZIONI = 20  # puoi mettere 15 o 20

def prendi_ultime_estrazioni(lista_estrazioni):
    """
    Ritorna solo le ultime N estrazioni
    """
    if not lista_estrazioni:
        return []
    return lista_estrazioni[-ULTIME_ESTRAZIONI:]