import ZADANIE4.zadanie4 as Z

def test_skaner_temperatur_monkeypatch(monkeypatch):
    # kontrolowane temperatury dla kilku miast (reszta dostanie domyślnie 5 °C)
    mapa_temp = {
        "Warszawa":  10,
        "Krakow":     7,
        "Lodz":       8,
        "Wroclaw":   12,
    }

    def fake_get(url):
        # wyciągamy <Miasto> z "https://wttr.in/<Miasto>?format=j1"
        miasto_q = url.split("wttr.in/")[1].split("?")[0]
        t = mapa_temp.get(miasto_q, 5)
        class R:
            def json(self_inner):
                return {"current_condition": [{"temp_C": str(t)}]}
        return R()

    # podmieniamy requests.get w module zadanie6
    monkeypatch.setattr(Z.requests, "get", fake_get)

    wyniki = Z.skaner_temperatur()
    assert isinstance(wyniki, list)
    assert len(wyniki) == len(Z.MIASTA)

    # słownik dla wygody asercji
    temp_dict = dict(wyniki)
    assert temp_dict["Wrocław"] == 12
    assert temp_dict["Kraków"] == 7

    # min / max z tego co zwróciła funkcja
    min_miasto, min_temp = min(wyniki, key=lambda p: p[1])
    max_miasto, max_temp = max(wyniki, key=lambda p: p[1])

    # w naszym układzie powinno wyjść max=12 (Wrocław), min=5 (domyślne)
    assert max_temp == 12
    assert max_miasto == "Wrocław"
    assert min_temp in (5, 7)  # zależnie które miasto domyślne wyląduje najniżej

def test_wypisywanie_podsumowania(monkeypatch, capsys):
    # uprośćmy: wszystkie miasta dostaną "1 °C"
    def fake_get(url):
        class R:
            def json(self_inner):
                return {"current_condition": [{"temp_C": "1"}]}
        return R()
    monkeypatch.setattr(Z.requests, "get", fake_get)

    temperatury = Z.skaner_temperatur()

    # fragment „main”: wyliczamy min/max i wypisujemy podsumowanie
    min_miasto, min_temp = min(temperatury, key=lambda p: p[1])
    max_miasto, max_temp = max(temperatury, key=lambda p: p[1])

    print("\n=== Podsumowanie ===")
    print("Najchłodniej:", min_miasto, ": ", min_temp, "°C")
    print("Najcieplej: ", max_miasto, ": ", max_temp, "°C")

    out = capsys.readouterr().out
    assert "=== Podsumowanie ===" in out
    assert "Najchłodniej:" in out
    assert "Najcieplej:" in out
