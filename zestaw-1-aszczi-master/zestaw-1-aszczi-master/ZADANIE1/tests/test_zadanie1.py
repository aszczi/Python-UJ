from ZADANIE1.zadanie1 import rozklad_na_czynniki

# Testy sprawdzające funkcję rozkładania na czynniki pierwsze z formatowaniem wyniku

def test_single_prime():
    liczba = 13
    wynik = rozklad_na_czynniki(liczba)
    assert wynik == "13", f"Błąd: Oczekiwano 13, otrzymano {wynik}"

def test_prime_product():
    liczba = 3 * 17
    wynik = rozklad_na_czynniki(liczba)
    assert wynik == "3*17", f"Błąd: Oczekiwano 3*17, otrzymano {wynik}"

def test_large_prime():
    liczba = 805037
    wynik = rozklad_na_czynniki(liczba)
    assert wynik == "805037", f"Błąd: Oczekiwano 805037, otrzymano {wynik}"

def test_power_of_two():
    liczba = 2**10
    wynik = rozklad_na_czynniki(liczba)
    assert wynik == "2^10", f"Błąd: Oczekiwano 2^10, otrzymano {wynik}"

def test_mixed_factors():
    liczba = (2**3) * (3**4) * (5**2)
    wynik = rozklad_na_czynniki(liczba)
    assert wynik == "2^3*3^4*5^2", f"Błąd: Oczekiwano 2^3*3^4*5^2, otrzymano {wynik}"

def test_edge_case_one():
    liczba = 1
    wynik = rozklad_na_czynniki(liczba)
    assert wynik == "", f"Błąd: Oczekiwano '', otrzymano {wynik}"

def test_large_composite():
    liczba = 13041599400
    wynik = rozklad_na_czynniki(liczba)
    assert wynik == "2^3*3^4*5^2*805037", f"Błąd: Oczekiwano 2^3*3^4*5^2*805037, otrzymano {wynik}"
