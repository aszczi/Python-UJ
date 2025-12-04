import types
import builtins
import requests
import pytest

import ZADANIE3.zadanie3 as zadanie3

# --- selekcja ---

def test_selekcja_podstawowe():
    txt = "Ala ma 3 koty i 2 psy oraz żółw"
    # tylko >=4 i same litery, lowercase
    out = zadanie3.selekcja(txt)
    assert out == ["koty", "oraz", "żółw"]

def test_selekcja_unicode_pl():
    txt = "Zażółć gęślą jaźń 1234"
    out = zadanie3.selekcja(txt)
    # >=4: "zażółć"(6), "gęślą"(5), "jaźń"(4)
    assert out == ["zażółć", "gęślą", "jaźń"]

def test_selekcja_ignores_short_and_digits():
    txt = "AAA bbb Cccc 123 abcde"
    out = zadanie3.selekcja(txt)
    # "AAA"(3) out, "bbb"(3) out, "Cccc"(4), "123" out, "abcde"(5)
    assert out == ["cccc", "abcde"]


# --- ramka ---

def test_ramka_center_and_width():
    s = zadanie3.ramka("Kot", width=10)
    # szerokość dokładnie 10, centrowanie w polu content_w=8: '  Kot   '
    assert len(s) == 10
    assert s == "[  Kot   ]"

@pytest.mark.parametrize("w", [10, 20, 80])
def test_ramka_truncation_ellipsis_and_brackets(w):
    long = "To jest bardzo długi tytuł, który trzeba przyciąć"
    framed = zadanie3.ramka(long, width=w)
    assert len(framed) == w
    assert framed.startswith("[") and framed.endswith("]")
    # jeśli za długie, powinno zawierać znak '…'
    content_w = max(0, w - 2)
    if len(long.strip()) > content_w:
        assert "…" in framed


# --- main() z monkeypatch requests.get oraz N ---

class _FakeResp:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data

def test_main_aggregates_and_retries(monkeypatch, capsys):
    # Ustaw N=3, żeby test był szybki i deterministyczny
    monkeypatch.setattr(zadanie3, "N", 3, raising=True)

    # Przygotuj sekwencję odpowiedzi: 1) wyjątek (retry), 2-4) poprawne
    seq = [
        Exception("timeout"),
        _FakeResp({"title": "Hasło A", "extract": "Ala ma kota"}),  # -> "kota"
        _FakeResp({"title": "Hasło B", "extract": "Python 3.13 jest super językiem"}),  # -> python, jest, super, językiem
        _FakeResp({"title": "Hasło C", "extract": "Żółw żółw żółw 123"}),  # -> żółw x3
    ]

    def fake_get(url, headers=None, timeout=None):
        item = seq.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    monkeypatch.setattr(requests, "get", fake_get, raising=True)

    # Skróć przerwy sleep do zera, żeby test był natychmiastowy
    monkeypatch.setattr(zadanie3.time, "sleep", lambda *_a, **_k: None, raising=True)

    # Uruchom main() i zbierz stdout
    zadanie3.main()
    out = capsys.readouterr().out

    # Sprawdź podsumowanie
    assert "Pobrano wpisów: 3" in out
    assert "Słów (≥4) łącznie:" in out
    assert "Unikalnych (≥4):" in out

    # Sprawdź, że top zawiera oczekiwane słowa (≥ 4 znaki):
    # z 3 ekstraktów: "kota" (1), "python"(1), "jest"(1), "super"(1), "językiem"(1), "żółw"(3)
    assert "żółw" in out
    assert "python" in out
    assert "kota" in out
    assert "językiem" in out


def test_main_prints_progress_frame(monkeypatch, capsys):
    # Ustaw N=1, jedna odpowiedź
    monkeypatch.setattr(zadanie3, "N", 1, raising=True)
    # Podmień requests.get
    monkeypatch.setattr(
        requests,
        "get",
        lambda *a, **k: _FakeResp({"title": "Testowy tytuł", "extract": "to tylko przykład przykładu"}),
        raising=True,
    )
    monkeypatch.setattr(zadanie3.time, "sleep", lambda *_a, **_k: None, raising=True)

    zadanie3.main()
    out = capsys.readouterr().out

    # Powinien pojawić się wydruk ramki kończący się nową linią
    assert "Pobrano wpisów: 1" in out
    assert "Top 15 słów (≥4):" in out
