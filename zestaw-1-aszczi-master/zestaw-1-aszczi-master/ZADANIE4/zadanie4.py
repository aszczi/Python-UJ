import requests

MIASTA = [
    ("Warszawa","Warszawa"),("Kraków","Krakow"),("Łódź","Lodz"),("Wrocław","Wroclaw"),
    ("Poznań","Poznan"),("Gdańsk","Gdansk"),("Szczecin","Szczecin"),("Bydgoszcz","Bydgoszcz"),
    ("Lublin","Lublin"),("Białystok","Bialystok"),("Katowice","Katowice"),("Gdynia","Gdynia"),
    ("Częstochowa","Czestochowa"),("Radom","Radom"),("Toruń","Torun"),
]

# Należy zdefiniować funkcję skaner_temperatur(), która zwraca listę krotek (miasto, temperatura_int)
# w tej samej kolejności co MIASTA. Źródłem danych jest serwis wttr.in (adres: https://wttr.in/NazwaMiasta?format=j1).
# Funkcja ma pobrać bieżącą temperaturę w °C (klucz "temp_C"), zamienić ją na int i zbudować listę wyników.
#
# Oczekiwane użycie w programie:
# - wywołanie skaner_temperatur(), wypisanie zestawienia "Miasto : temperatura °C" w oddzielnych liniach,
# - wyznaczenie miasta z najniższą i najwyższą temperaturą (nazwy i wartości) na podstawie zwróconej listy,
# - przypisanie wyników do zmiennych: min_miasto, min_temp, max_miasto, max_temp.

def skaner_temperatur():

    wyniki = []
    
    for miasto_pol, miasto_ang in MIASTA:
        try:
            # Pobieranie danych z API
            url = f"https://wttr.in/{miasto_ang}?format=j1"
            response = requests.get(url)
            data = response.json()
            
            # Pobieranie temperatury
            temp_c = data['current_condition'][0]['temp_C']
            temperatura_int = int(temp_c)
            
            wyniki.append((miasto_pol, temperatura_int))
            
        except Exception as e:
            print(f"Błąd dla miasta {miasto_pol}: {e}")
            wyniki.append((miasto_pol, None))  # fallback
    
    return wyniki

if __name__ == "__main__":
    # twoj kod
    wyniki = skaner_temperatur()
    min_miasto = wyniki[0][0]
    min_temp = wyniki[0][1]
    max_miasto = wyniki[0][0]
    max_temp = wyniki[0][1]

    for klucz, wartosc in wyniki:
        if(min_temp > wartosc):
            min_temp = wartosc
            min_miasto = klucz
        if(max_temp < wartosc):
            max_temp = wartosc
            max_miasto = klucz
        print(f"{klucz} : {wartosc} °C")
              
    print("\n=== Podsumowanie ===")
    print("Najchłodniej:", min_miasto, ": ", min_temp, "°C")
    print("Najcieplej: ", max_miasto, ": ", max_temp, "°C")
