"""
Zegar — HH : MM : SS (24h) 

Matryce cyfr i dwukropka zbudowane są z '█' i spacji (8×8 dla cyfr, 8×4 dla ':').
"""
import os
import time
from datetime import datetime

# Ustawienia
FPS = 4               # klatki/sekundę
DIGIT_H = 8           # wysokość (wiersze)
PRZERWA = 2           # odstęp (kolumny)

# Wzorce cyfr (każdy wiersz ma szerokość 8 znaków)
DIGITS = {
    '0': [
        "████████",
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        "██    ██",
        "████████",
    ],
    '1': [
        "    ███ ",
        "   ████ ",
        "    ███ ",
        "    ███ ",
        "    ███ ",
        "    ███ ",
        "    ███ ",
        "  ██████",
    ],
    '2': [
        "████████",
        "      ██",
        "      ██",
        "████████",
        "██      ",
        "██      ",
        "██      ",
        "████████",
    ],
    '3': [
        "████████",
        "      ██",
        "      ██",
        "████████",
        "      ██",
        "      ██",
        "      ██",
        "████████",
    ],
    '4': [
        "██    ██",
        "██    ██",
        "██    ██",
        "████████",
        "      ██",
        "      ██",
        "      ██",
        "      ██",
    ],
    '5': [
        "████████",
        "██      ",
        "██      ",
        "████████",
        "      ██",
        "      ██",
        "      ██",
        "████████",
    ],
    '6': [
        "████████",
        "██      ",
        "██      ",
        "████████",
        "██    ██",
        "██    ██",
        "██    ██",
        "████████",
    ],
    '7': [
        "████████",
        "      ██",
        "     ██ ",
        "    ██  ",
        "   ██   ",
        "  ██    ",
        "  ██    ",
        "  ██    ",
    ],
    '8': [
        "████████",
        "██    ██",
        "██    ██",
        "████████",
        "██    ██",
        "██    ██",
        "██    ██",
        "████████",
    ],
    '9': [
        "████████",
        "██    ██",
        "██    ██",
        "████████",
        "      ██",
        "      ██",
        "      ██",
        "████████",
    ],
}

COLON = [
    "    ",
    " ██ ",
    " ██ ",
    "    ",
    "    ",
    " ██ ",
    " ██ ",
    "    ",
]



def czyszczenie():
    """Wyczyść ekran poleceniami systemu. 
    Wskazówka: os.name == 'nt' → os.system('cls'), w przeciwnym razie os.system('clear').
    """
    if os.name == 'nt':
        os.system('cls')  
    else:
        os.system('clear') 


def klatka(dt: datetime) -> str: 
    # Zbuduj i zwróć wieloliniowy napis czasu w formacie HH : MM : SS
    # korzystając z DIGITS i COLON. Pamiętaj o PRZERWA między znakami i DIGIT_H wierszy.
    godzina = str(dt.hour).zfill(2) 
    minuta = str(dt.minute).zfill(2) 
    sekunda = str(dt.second).zfill(2) 
    time_str = godzina + ":" + minuta + ":" + sekunda
    wiersze = ["" for _ in range(DIGIT_H)]

    for znak in time_str:
        if znak == ":":
            matryca = COLON
        else:
            matryca = DIGITS[znak]

        for i in range(DIGIT_H):
            wiersze[i] += matryca[i] + (" " * PRZERWA)

    return "\n".join(wiersze)

   

def rysuj():
    delay = 1.0 / max(1, FPS)
    while True:
        now = datetime.now()
        czyszczenie()
        print(klatka(now), flush=True)
        time.sleep(delay)


if __name__ == "__main__":
    rysuj()
