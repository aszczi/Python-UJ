def rzymskie_na_arabskie(rzymskie):
    # twój kod
    if not isinstance(rzymskie, str):
            raise TypeError(f"Oczekiwano typu str, otrzymano: {type(rzymskie).__name__}")
        
    rzymskie = rzymskie.upper()

    mapa_znakow = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}

    if not rzymskie:
            raise ValueError("Ciąg znaków nie może być pusty.")
            
    for znak in rzymskie:
          if znak not in mapa_znakow:
              raise ValueError(f"Niedozwolony znak w liczbie rzymskiej: {znak}")
    wartosc = 0
    poprzedni_znak = 0
        
    for char in reversed(rzymskie):
        znak_po_znaku = mapa_znakow[char]
        if znak_po_znaku < poprzedni_znak:
            wartosc -=  znak_po_znaku
        else:
             wartosc += znak_po_znaku
        poprzedni_znak = znak_po_znaku
    try:
            poprawny_rzymski = arabskie_na_rzymskie(wartosc)
            if poprawny_rzymski != rzymskie:
                raise ValueError(f"Niepoprawny format liczby rzymskiej: '{rzymskie}' (powinno być: '{poprawny_rzymski}')")
    except ValueError as e:
        raise ValueError(f"Błąd walidacji liczby rzymskiej: {e}")
    return wartosc

def arabskie_na_rzymskie(arabskie):
    # twój kod
    if not isinstance(arabskie, int):
        raise TypeError(f"Oczekiwano typu int, otrzymano: {type(arabskie).__name__}")
        
    if not (1 <= arabskie <= 3999):
        raise ValueError(f"Liczba {arabskie} jest poza zakresem 1-3999.")

    wartosci = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    
    wynik = []
    
    for wartosc, symbol in wartosci:
        while arabskie >= wartosc:
            wynik.append(symbol)
            arabskie -= wartosc
            
    rzymskie = "".join(wynik)

    return rzymskie

if __name__ == '__main__':
    try:
        # Przykłady konwersji rzymskiej na arabską
        rzymska = "MCMXCIV"
        print(f"Liczba rzymska {rzymska} to {rzymskie_na_arabskie(rzymska)} w arabskich.")
        
        # Przykłady konwersji arabskiej na rzymską
        arabska = 1994
        print(f"Liczba arabska {arabska} to {arabskie_na_rzymskie(arabska)} w rzymskich.")
        
    except ValueError as e:
        print(e)
