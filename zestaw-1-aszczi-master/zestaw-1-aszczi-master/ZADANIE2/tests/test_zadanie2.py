import ZADANIE2.zadanie2 as sg


def rle_len(seq: str) -> int:
    # Pomocnicza wersja liczenia długości RLE dla całego ciągu
    if not seq:
        return 0
    total = 0
    curr = seq[0]
    count = 1
    for ch in seq[1:]:
        if ch == curr:
            count += 1
        else:
            total += sg.dlugosc(count)
            curr = ch
            count = 1
    total += sg.dlugosc(count)
    return total


def compression_percent(seq: str) -> int:
    if not seq:
        return 100
    return round(100 * rle_len(seq) / len(seq))


def test_dlugosc_basic():
    assert sg.dlugosc(1) == 1
    assert sg.dlugosc(2) == 2  # "a2"
    assert sg.dlugosc(9) == 2  # "a9"
    assert sg.dlugosc(10) == 3  # "a10"


def test_rle_len_and_percent_examples():
    assert rle_len("") == 0
    assert rle_len("a") == 1
    assert rle_len("aa") == 2
    assert rle_len("aaa") == 2  # "a3"
    assert rle_len("aaabbbc") == 5  # "a3b3c"

    assert compression_percent("a") == 100
    assert compression_percent("aa") == 100
    assert compression_percent("aaa") == 67  # 2/3 -> 66.6 -> 67
    assert compression_percent("aaabbbc") == 71  # 5/7 -> 71.4 -> 71


def test_online_percent_prefixes():
    seq = "aaabbbc"
    prefixes = [seq[:i] for i in range(1, len(seq) + 1)]
    percents = [compression_percent(p) for p in prefixes]
    # Oczekiwane: a, aa, aaa, aaab, aaabb, aaabbb, aaabbbc
    assert percents == [100, 100, 67, 75, 80, 67, 71]


def test_znaki_run_length_range(monkeypatch):
    # Wymuszamy dlugosc ciągu 3 i naprzemienne znaki A/B, aby zobaczyc granice ciągów
    run = {"i": -1}

    def fake_choice(_alphabet):
        run["i"] += 1
        return "A" if run["i"] % 2 == 0 else "B"

    def fake_randint(a, b):
        # Powinno byc 1..10
        assert a == 1 and b == 10
        return 3

    monkeypatch.setattr(sg.random, "choice", fake_choice)
    monkeypatch.setattr(sg.random, "randint", fake_randint)

    it = sg.znaki()
    out = [next(it) for _ in range(8)]  # 3xA, 3xB, 2xA
    assert out == list("AAABBBAA")
