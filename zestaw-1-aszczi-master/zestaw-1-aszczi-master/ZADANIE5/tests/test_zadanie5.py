import ZADANIE5.zadanie5 as mod

def test_pobierz_odpowiedz_monkeypatch(monkeypatch):
    
    def fake_post(url, json):
        class R:
            def json(self_inner):
                return {"response": "FAKE_ODPOWIEDŹ"}
        return R()

    monkeypatch.setattr(mod.requests, "post", fake_post)

    txt = mod.pobierz_odpowiedz("Jakie jest 2+2?")
    assert isinstance(txt, str)
    assert txt == "FAKE_ODPOWIEDŹ"

def test_uruchom_czat_jeden_obrot(monkeypatch, capsys):

    # symulujemy jedno pytanie i zakończenie (pusty ENTER)
    wejscia = iter(["Cześć modelu!", ""])

    def fake_input(prompt=""):
        return next(wejscia)

    def fake_post(url, json):
        class R:
            def json(self_inner):
                return {"response": "Witaj! To odpowiedź testowa."}
        return R()

    monkeypatch.setattr("builtins.input", fake_input)
    monkeypatch.setattr(mod.requests, "post", fake_post)

    mod.uruchom_czat()

    out = capsys.readouterr().out
    assert "Prosty czat z lokalnym modelem" in out
    assert "Model: Witaj! To odpowiedź testowa." in out
