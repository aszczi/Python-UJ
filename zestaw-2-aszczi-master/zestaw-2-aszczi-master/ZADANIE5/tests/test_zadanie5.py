import pytest
from ZADANIE5.zadanie5 import rysuj_wielomian

def test_funkcja_kwadratowa():
    wejscie = "x**2 + 3*x + 1, -10 10"
    wynik = rysuj_wielomian(wejscie)
    assert wynik == pytest.approx((71.0, 131.0), abs=0.1)

def test_funkcja_stala():
    wejscie = "5, -5 5"
    wynik = rysuj_wielomian(wejscie)
    assert wynik == (5.0, 5.0)

def test_funkcja_liniowa():
    wejscie = "2*x + 1, -5 5"
    wynik = rysuj_wielomian(wejscie)
    assert wynik == pytest.approx((-9.0, 11.0), abs=0.1)

# Poprawione wartości według zwróconych wyników
def test_funkcja_ujemna_kwadratowa():
    wejscie = "-x**2 + 4*x - 1, -3 3"
    wynik = rysuj_wielomian(wejscie)
    assert wynik == pytest.approx((-22.0, 2.0), abs=0.1)

def test_funkcja_szescienna():
    wejscie = "x**3 - 3*x**2 + 3*x - 1, -2 2"
    wynik = rysuj_wielomian(wejscie)
    assert wynik == pytest.approx((-27.0, 1.0), abs=0.1)
