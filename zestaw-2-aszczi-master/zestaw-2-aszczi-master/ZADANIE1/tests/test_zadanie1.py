from ZADANIE1.zadanie1 import dodaj_element

def test_pojedyncza_zagniezdzona_lista():
    structure = [1, [2, 3], 4]
    expected = [1, [2, 3, 4], 4]
    assert dodaj_element(structure) == expected

def test_wiele_zagniezdzonych_list():
    structure = [1, [3], [2]]
    expected = [1, [3, 4], [2, 3]]
    assert dodaj_element(structure) == expected

def test_gleboko_zagniezdzona_struktura_z_pustymi_listami():
    structure = [[], {"a": ()}, [1, 2, 3, 4]]
    expected = [[1], {"a": ()}, [1, 2, 3, 4, 5]]
    assert dodaj_element(structure) == expected

def test_struktura_zlozona_z_slownikami_i_krotkami():
    structure = [
        1, 2, [3, 4, [5, {"klucz": [5, 6], "tekst": [1, 2]}], 5],
        "hello", 3, [4, 5], (5, (6, (1, [7, 8])))
    ]
    expected = [
        1, 2, [3, 4, [5, {"klucz": [5, 6, 7], "tekst": [1, 2, 3]}], 5],
        "hello", 3, [4, 5], (5, (6, (1, [7, 8, 9])))
    ]
    assert dodaj_element(structure) == expected

def test_pusta_najglebsza_lista():
    structure = [1, 2, [[], {"klucz": [], "tekst": []}], 3]
    expected = [1, 2, [[], {"klucz": [1], "tekst": [1]}], 3]
    assert dodaj_element(structure) == expected

def test_jedyna_pusta_lista():
    structure = [[]]
    expected = [[1]]
    assert dodaj_element(structure) == expected

def test_wiele_pustych_list():
    structure = [[], [[], []]]
    expected = [[], [[1], [1]]]
    assert dodaj_element(structure) == expected

def test_zagniezdzone_puste_i_niepuste_listy():
    structure = [[1, 2], [], [3, [4, []]]]
    expected = [[1, 2], [], [3, [4, [1]]]]
    assert dodaj_element(structure) == expected

def test_zlozona_struktura_z_roznych_typow():
    structure = [
        "hello", 3.5, [1, 2, [], {"data": [7, 8, []]}], (5, [6, (7, [8, 9])])
    ]
    expected = [
        "hello", 3.5, [1, 2, [], {"data": [7, 8, [1]]}], (5, [6, (7, [8, 9, 10])])
    ]
    assert dodaj_element(structure) == expected

def test_bez_zagniezdzenia():
    structure = [1, 2, 3, 4]
    expected = [1, 2, 3, 4, 5]  # Dodajemy 5 do jedynej listy
    assert dodaj_element(structure) == expected
