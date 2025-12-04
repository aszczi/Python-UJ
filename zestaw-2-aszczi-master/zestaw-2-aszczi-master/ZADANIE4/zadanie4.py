import os
import time
import threading
import sys

# Stałe konfiguracyjne
LICZBA_KROKOW = 80_000_000
LICZBA_WATKOW = sorted({1, 2, 4, os.cpu_count() or 4})


def policz_fragment_pi(pocz: int, kon: int, krok: float, wyniki: list[float], indeks: int) -> None:
    # Funkcja oblicza częściową sumę przybliżenia liczby pi metodą prostokątów.
    # Argumenty:
    #     pocz, kon - zakres iteracji (indeksy kroków całkowania),
    #     krok      - szerokość pojedynczego prostokąta (1.0 / LICZBA_KROKOW),
    #     wyniki    - lista, do której należy wpisać wynik dla danego wątku na pozycji indeks,
    #     indeks    - numer pozycji w liście 'wyniki' do zapisania rezultatu.

    # Każdy wątek powinien:
    #   - obliczyć lokalną sumę dla przydzielonego przedziału,
    #   - wpisać wynik do wyniki[indeks].

    # zaimplementuj obliczanie fragmentu całki dla danego wątku
    suma_czesciowa = 0.0
    
    for i in range(pocz, kon):
        x = (i + 0.5) * krok
        suma_czesciowa += 4.0 / (1.0 + x * x)
    
    wyniki[indeks] = suma_czesciowa


def main():
    print(f"Python: {sys.version.split()[0]}  (tryb bez GIL? {getattr(sys, '_is_gil_enabled', lambda: None)() is False})")
    print(f"Liczba rdzeni logicznych CPU: {os.cpu_count()}")
    print(f"LICZBA_KROKOW: {LICZBA_KROKOW:,}\n")

    # Wstępne uruchomienie w celu stabilizacji środowiska wykonawczego
    krok = 1.0 / LICZBA_KROKOW
    wyniki = [0.0]
    w = threading.Thread(target=policz_fragment_pi, args=(0, LICZBA_KROKOW, krok, wyniki, 0))
    w.start()
    w.join()

    # ---------------------------------------------------------------
    # Tu zaimplementować:
    #   - utworzenie wielu wątków (zgodnie z LICZBY_WATKOW),
    #   - podział pracy na zakresy [pocz, kon) dla każdego wątku,
    #   - uruchomienie i dołączenie wątków (start/join),
    #   - obliczenie przybliżenia π jako sumy wyników z poszczególnych wątków,
    #   - pomiar czasu i wypisanie przyspieszenia.
    # ---------------------------------------------------------------

    czas_referencyjny = None

    for n_watkow in LICZBA_WATKOW:
        wyniki = [0.0] * n_watkow
        watki = []

        start_time = time.perf_counter()

        for i in range(n_watkow):
            pocz = (i * LICZBA_KROKOW) // n_watkow
            kon = ((i + 1) * LICZBA_KROKOW) // n_watkow
            
            t = threading.Thread(
                target=policz_fragment_pi, 
                args=(pocz, kon, krok, wyniki, i)
            )
            watki.append(t)
            t.start()

        for t in watki:
            t.join()
            
        end_time = time.perf_counter()        
        czas_trwania = end_time - start_time
        pi_total = sum(wyniki) * krok
        
        if n_watkow == 1:
            czas_referencyjny = czas_trwania
            przyspieszenie = 1.00
        else:
            przyspieszenie = czas_referencyjny / czas_trwania if czas_referencyjny else 0.0

        # Wypisanie wyników
        print(f"Liczna wątków: {n_watkow:<10}    Czas trwania:{czas_trwania:<15.4f}    Przyspieszenie: {przyspieszenie:<15.2f}x    π ≈ {pi_total:<20.10f}")

if __name__ == "__main__":
    main()
