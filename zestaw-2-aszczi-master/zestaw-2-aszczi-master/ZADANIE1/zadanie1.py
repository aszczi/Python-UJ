def dodaj_element(wejscie):
    # może warto zdefiniować zagnieżdżoną funkcję
    
    def znajdywanie_maks_glebokosci(obj, poziom):
        maks_gl = -1
    
        if isinstance(obj, list):
            maks_gl = poziom

        if isinstance(obj, dict):
            for wartosc in obj.values():
                glebokosc_dziecka = znajdywanie_maks_glebokosci(wartosc, poziom + 1)
                maks_gl = max(maks_gl, glebokosc_dziecka)
                    
        if isinstance(obj, (list, tuple)):
            for element in obj:
                glebokosc_dziecka = znajdywanie_maks_glebokosci(element, poziom + 1)
                maks_gl = max(maks_gl, glebokosc_dziecka)
        
        return maks_gl

    def modyfikacja_na_poziomie(obj, poziom):
        if isinstance(obj, list) and poziom == maks_poziom:
            nowy_element = 1
            if len(obj) > 0 and isinstance(obj[-1], int):
                nowy_element = obj[-1] + 1
            
            obj.append(nowy_element)
            return

        if isinstance(obj, dict):
            for wartosc in obj.values():
                modyfikacja_na_poziomie(wartosc, poziom + 1)
                
        if isinstance(obj, (list, tuple)):
            for element in obj:
                modyfikacja_na_poziomie(element, poziom + 1)

    maks_poziom = znajdywanie_maks_glebokosci(wejscie, 0)
    modyfikacja_na_poziomie(wejscie, 0)

    return wejscie

if __name__ == '__main__':
    input_list = [
     1, 2, [3, 4, [5, {"klucz": [5, 6], "tekst": [1, 2]}], 5],
     "hello", 3, [4, 5], 5, (6, (1, [7, 8]))
    ]
    output_list = dodaj_element(input_list)
    print(input_list)   
