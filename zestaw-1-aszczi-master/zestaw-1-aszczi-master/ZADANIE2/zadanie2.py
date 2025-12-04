"""
Generator strumienia znaków + liczony "w locie" współczynnik
kompresji RLE. Założenia:
- Alfabet: A-Z, a-z.
- Każdy ciąg jednakowych znaków ma długość losowaną z zakresu 1–10.
- Wydruk: jedna linia (ostatnie WIDTH znaków) + procent kompresji.
- Brak wyjątków; generacja zatrzymuje się po MAXLEN znakach.

Uwaga: animacja w jednej linii powinna być zrealizowana przez print(..., end="\r", flush=True),
a do czyszczenia „resztek” w obrębie okna – przez ljust(WIDTH). Na końcu stały sufiks "  {:3d}%".
"""

import random
import string
import time
from collections import deque

WIDTH = 80            # szerokość okna podglądu
MAXLEN = 1000         # maksymalna liczba generowanych znaków
DELAY_SEC = 0.02      # opóźnienie między kolejnymi znakami (płynność animacji)

ALPHABET = string.ascii_letters  # A-Z, a-z

def znaki():
    """
    Generator znaków:
      - losuje znak z ALPHABET (random.choice(ALPHABET))
      - losuje liczbę powtórzeń 1..10 (random.randint(1, 10))
      - yielduje wylosowany znak tyle razy
    Pętla powinna działać w nieskończoność (while True).
    """
    while True:
        ch = random.choice(ALPHABET)
        repeat = random.randint(1, 10)
        for _ in range(repeat):
            yield ch


def dlugosc(count: int) -> int:
    """
    Zwraca długość zapisu RLE dla runu długości `count` (single-run rule):
      - jeśli count == 1 → 1 (pojedynczy znak),
      - jeśli count >= 2 → 1 + len(str(count)).
    """
    if count == 1:
        return 1
    else:
        return 1 + len(str(count))


def main():
    """
    Główny kod wyświetlający animację i wartość kompresji.
    """
    buf = deque(maxlen=WIDTH)

    # Główna pętla:
    # for ch in znaki():
    #     ...
    #     if total_raw >= MAXLEN:
    #         break

    total_raw = 0
    total_compressed = 0
    
    for ch in znaki():
        buf.append(ch)
        total_raw += 1

        if buf:
            current_compressed = 0
            current_char = buf[0]
            current_count = 1
            
            for i in range(1, len(buf)):
                if buf[i] == buf[i-1]:
                    current_count += 1
                else:
                    current_compressed += dlugosc(current_count)
                    current_char = buf[i]
                    current_count = 1
            
            current_compressed += dlugosc(current_count)
            total_compressed = current_compressed
        
        #blicza procent kompresji
        if total_raw > 0:
            compression_ratio = int((total_compressed / total_raw) * 100)
        else:
            compression_ratio = 0
        
        # Animacja
        line = "".join(buf).ljust(WIDTH)
        print(f"{line}  {compression_ratio:3d}%", end="\r", flush=True)
        
        time.sleep(DELAY_SEC)
        
        if total_raw >= MAXLEN:
            break

    # Po zakończeniu animacji:
    print()


if __name__ == "__main__":
    main()
