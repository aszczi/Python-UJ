import math
import types
import pytest
import ZADANIE4.zadanie4 as z4


def test_ma_funkcje_main():
    """Sprawdza, czy moduł posiada funkcję main()"""
    assert hasattr(z4, "main")
    assert isinstance(z4.main, types.FunctionType)


def test_ma_funkcje_policz_fragment_pi():
    """Sprawdza, czy funkcja policz_fragment_pi istnieje i przyjmuje poprawne argumenty"""
    assert hasattr(z4, "policz_fragment_pi")
    fn = z4.policz_fragment_pi
    assert callable(fn)
    # Funkcja powinna mieć pięć argumentów: pocz, kon, krok, wyniki, indeks
    assert fn.__code__.co_argcount == 5


def test_przyblizenie_pi_jednowatkowe():
    """Dla jednego wątku wynik powinien być bliski wartości referencyjnej pi"""
    krok = 1.0 / 1_000_000  # 1e6 iteracji wystarczy do stabilnego testu
    wyniki = [0.0]
    z4.policz_fragment_pi(0, 1_000_000, krok, wyniki, 0)
    przybl = krok * wyniki[0]
    assert math.isclose(przybl, math.pi, rel_tol=1e-6, abs_tol=1e-6)


def test_podzial_zakresu_wielowatkowo():
    """Sprawdza, czy łączenie wyników z kilku fragmentów daje poprawny wynik"""
    liczba_krokow = 1_000_000
    krok = 1.0 / liczba_krokow
    n = 4
    podstawa = liczba_krokow // n
    zakresy = []
    start = 0
    for k in range(n):
        end = start + podstawa + (1 if k < (liczba_krokow % n) else 0)
        zakresy.append((start, end))
        start = end

    wyniki = [0.0] * n
    watki = [
        z4.threading.Thread(
            target=z4.policz_fragment_pi, args=(p, q, krok, wyniki, k)
        )
        for k, (p, q) in enumerate(zakresy)
    ]
    for w in watki:
        w.start()
    for w in watki:
        w.join()

    przybl = krok * sum(wyniki)
    assert math.isclose(przybl, math.pi, rel_tol=1e-6, abs_tol=1e-6)


def test_wynik_deterministyczny():
    """Symulacja małego zakresu - wynik powinien być powtarzalny"""
    wyniki = [0.0]
    krok = 1.0 / 1000
    z4.policz_fragment_pi(0, 1000, krok, wyniki, 0)
    wynik1 = wyniki[0]

    wyniki = [0.0]
    z4.policz_fragment_pi(0, 1000, krok, wyniki, 0)
    wynik2 = wyniki[0]

    assert wynik1 == pytest.approx(wynik2, rel=0, abs=0)


def test_main_nie_rzuca(monkeypatch):
    """Funkcja main() powinna się wykonać bez wyjątków (szybka wersja dla CI)"""
    # Zmniejszamy liczbę kroków, by test trwał krótko w środowisku CI
    monkeypatch.setattr(z4, "LICZBA_KROKOW", 200_000)
    z4.main()
