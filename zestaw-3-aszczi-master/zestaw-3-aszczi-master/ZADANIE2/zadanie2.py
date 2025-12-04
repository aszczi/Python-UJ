import json
import folium


def process_tram_data(input_file):
    """
    Args:
        input_file (str): scieĹźka do pliku wesciowego JSON
    Returns:
        - statystyki: {numer_linii: liczba_przystankĂłw}
        - liczba_unikalnych_przystankĂłw: int
    """
    # Wczytaj dane z pliku input_file
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # StwĂłrz lownik ze statystykami {linia: liczba_przystankĂłw}
    stats = {}
    
    # ZnajdĹş wszystkie unikalne przystanki (uĹźyj set)
    unikalne_przystanki = set()
    
    # PrzejdĹş przez wszystkie linie i policz przystanki
    for linia_info in data['linie']:
        try:
            numer_linii = int(linia_info['linia'])
        except ValueError:
            numer_linii = linia_info['linia']
            
        lista_przystankow = linia_info['przystanki']
        
        stats[numer_linii] = len(lista_przystankow)

        for przystanek in lista_przystankow:
            unikalne_przystanki.add(przystanek['nazwa'])

    # Wypisz statystyki posortowane malejaco po liczbie przystankĂłw
    # Format: "linia X: Y"
    posortowane = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    for linia, liczba in posortowane:
        print(f"linia {linia}: {liczba}")
   
    # ZwrĂc wyniki
    return stats, len(unikalne_przystanki)  # przyklad


def create_tram_map(input_file, output_map_file):
    """
    Tworzy interaktywna mape sieci tramwajowej.
    Args:
        input_file (str): scieĹźka do pliku wesciowego JSON
        output_map_file (str): scieĹźka do pliku wysciowego HTML
    Przyklad:
        create_tram_map('linie_tramwajowe.json', 'mapa_tramwaje.html')
    """
    # Wczytaj dane
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    # StwĂłrz mae wycentrowana na Krakowie [50.06, 19.95], zoom=12
    m = folium.Map(location=[50.06, 19.95], zoom_start=12, tiles="cartodbpositron")

    # Paleta kolorĂłw dla rĂłĹźnych linii
    kolory = [
        "#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00",
        "#a65628", "#f781bf", "#999999", "#66c2a5", "#fc8d62",
        "#8da0cb", "#e78ac3", "#a6d854", "#ffd92f", "#e5c494",
        "#b3b3b3"
    ]

    # StwĂłrz lownik przystanek -> lista linii
    stop_to_lines = {}
    
    # Narysuj linie tramwajowe - dodaj PolyLine
    for i, linia_info in enumerate(data['linie']):
        numer_linii = linia_info['linia']
        przystanki = linia_info['przystanki']
        
        coordinates = []
        for p in przystanki:
            lat = p['lat']
            lon = p['lon']
            nazwa = p['nazwa']
            coordinates.append((lat, lon))
            
            if nazwa not in stop_to_lines:
                stop_to_lines[nazwa] = {'lat': lat, 'lon': lon, 'lines': set()}
            stop_to_lines[nazwa]['lines'].add(numer_linii)

        color = kolory[i % len(kolory)]
        
        folium.PolyLine(
            locations=coordinates,
            color=color,
            weight=3,
            opacity=0.9,
            tooltip=f"Linia {numer_linii}"
        ).add_to(m)



    # Dodaj markery dla przystankĂłw
    # Dla kaĹźdego unikalnego przystanku:
    #   - StwĂłrz CircleMarker
    #   - Dodaj tooltip z nazwa i lista linii
    for nazwa, info in stop_to_lines.items():
        linie_list = sorted(list(info['lines']), key=lambda x: int(x) if x.isdigit() else x)
        linie_str = ", ".join(linie_list)
        
        tooltip_text = f"{nazwa} – linie: {linie_str}"
        
        folium.CircleMarker(
            location=[info['lat'], info['lon']],
            radius=4,           
            color='black',    
            weight=1,
            fill=True,
            fill_color='white',  
            fill_opacity=1,
            tooltip=tooltip_text
        ).add_to(m)

    # Zapisz mape do pliku
    m.save(output_map_file)


def main():
    print("=" * 60)
    print("Analiza sieci tramwajowej w Krakowie")
    print("=" * 60)
    print()

    print("-" * 60)
    stats, unique_stops = process_tram_data('linie_tramwajowe.json')
    print(f"\nLiczba unikalnych przystankĂłw: {unique_stops}")
    print()

    print("-" * 60)
    create_tram_map('linie_tramwajowe.json', 'mapa_tramwaje.html')
    print(f"Wygenerowano mape: mapa_tramwaje.html")
    print()


if __name__ == "__main__":
    main()

