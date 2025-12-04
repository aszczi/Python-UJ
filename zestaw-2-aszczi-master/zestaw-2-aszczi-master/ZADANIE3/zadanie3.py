import requests, re, time, sys
from collections import Counter

URL = "https://pl.wikipedia.org/api/rest_v1/page/random/summary"
N = 100  # liczba losowań
HEADERS = {
    "User-Agent": "wp-edu-wiki-stats/0.1 (kontakt: twoj-email@domena)",
    "Accept": "application/json",
}

# przygotowanie wyrażenia regularnego wyłapującego słowa (litery)
WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def selekcja(text: str):
    # Wskazówka:
    #  użyj WORD_RE.findall(text), następnie przefiltruj wynik
    znalezione = WORD_RE.findall(text)
    
    # Zwróć listę słów wydobytych z 'text', spełniających warunki zadania:
    #  - słowa zapisane małymi literami
    #  - długość każdego słowa > 3 znaki
    wynik = [s.lower() for s in znalezione if len(s) > 3]
    # Przykład:
    #  selekcja("Ala ma 3 koty i 2 psy oraz żółw")
    #     -> ["koty", "oraz", "żółw"]

    return wynik

def ramka(text: str, width: int = 80) -> str:
    # Zwróć napis w ramce o stałej szerokości, w postaci:
    #   [        treść wyśrodkowana w polu o szerokości width-2       ]
    szerokosc_wewnetrzna = width - 2
    # Jeśli text jest za długi (ma więcej znaków niż width-2),
    # obetnij go do width-3 i dodaj na końcu znak '…' (U+2026).
    if len(text) > szerokosc_wewnetrzna:
        text = text[:width - 3] + "…"
    # Następnie wyśrodkuj (użyj str.center(...)) i doklej nawiasy
    # kwadratowe po bokach. Zwróć wynik w postaci f"[{...}]".
    wysrodkowane = text.center(szerokosc_wewnetrzna)
    # Przykład:
    #   ramka("Kot", width=10)  ->  "[  Kot   ]"   (łącznie 10 znaków)
    return f"[{wysrodkowane}]"


def main():
    cnt = Counter()
    licznik_slow = 0
    pobrane = 0

    # linia statusu
    print(ramka("Start"), end="", flush=True)

    while pobrane < N:
        try:
            data = requests.get(URL, headers=HEADERS, timeout=10).json()
        except Exception:
            # timeout / brak JSON → spróbuj ponownie
            time.sleep(0.1)
            continue

        # Pobierz tytuł hasła z 'data' (klucz "title"; jeśli brak, użyj pustego łańcucha)
        title = data.get("title", "")
    
        # Następnie drukuj ramkę z tym tytułem:
        #  - zbuduj łańcuch: "\r" + ramka(tytul, 80)
        #  - wydrukuj print(..., end="", flush=True), by nadpisywać bieżącą linię w konsoli
        line = "\r" + ramka(title, 80)
        print(line, end="", flush=True)
        
        # Przykład:
        #   title = data.get("title") or ""
        #   line = "\r" + ramka(title, 80)
        #   print(line, end="", flush=True)

        # Pobierz 'extract' (klucz "extract"; jeśli brak, użyj ""), przepuść przez selekcja()
        extract = data.get("extract", "")
        slowa = selekcja(extract)
        #  - wynikowa lista słów (>=4) powinna zostać doliczona do licznika:
        #       cnt.update(lista_slow)
        cnt.update(slowa)
        #  - dolicz też do licznik_slow długość tej listy
        licznik_slow += len(slowa)
        #  - zwiększ licznik 'pobrane' (udało się przetworzyć jedną próbkę)
        pobrane += 1
        #  - opcjonalnie mała przerwa: time.sleep(0.05)
        time.sleep(0.05)


    print(f"Pobrano wpisów: {pobrane}")
    print(f"Słów (≥4) łącznie:  {licznik_slow}")
    print(f"Unikalnych (≥4): {len(cnt)}\n")

    print("Top 15 słów (≥4):")
    # tu wypisz w pętli, korzystając np. z most_common(15)
    for slowo, licznosc in cnt.most_common(15):
        print(f"{slowo}: {licznosc}")

if __name__ == "__main__":
    main()
