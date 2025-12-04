import sys

# Funkcja do rozkładania liczby na czynniki pierwsze i formatowania wyniku
def rozklad_na_czynniki(n):
    if n < 1:
        return str(n)
    if n == 1:
        return ""
    
    result = ""
    k = 2
    slownik = {}
    
    # Szukanie dzielników
    while n > 1:
        count = 0
        while n % k == 0:  # dopóki liczba jest podzielna przez k
            n //= k
            count += 1
        
        if count > 0:
            slownik[k] = count
        k += 1

    # Formatowanie wyniku
    czynniki = []
    for klucz, wartosc in slownik.items():
        if wartosc > 1:
            czynniki.append(f"{klucz}^{wartosc}")
        else:
            czynniki.append(f"{klucz}")
    
    result = "*".join(czynniki)
    return result

# Główna funkcja programu
if __name__ == "__main__":
    argv = sys.argv[1:]  # Pobieranie argumentów zewnętrznych (liczby)

    for arg in argv:
        liczba = int(arg)
        wynik = rozklad_na_czynniki(liczba)
        print(f"{liczba} = {wynik}")
