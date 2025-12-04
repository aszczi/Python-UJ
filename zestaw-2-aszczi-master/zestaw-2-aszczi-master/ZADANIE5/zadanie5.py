import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify

# Funkcja rysująca wykres na podstawie eval()
def rysuj_wielomian(wejscie):

    wspolczynnik_funkcji, zakres = wejscie.split(',')
    x_min_str, x_max_str = zakres.strip().split()
    x_min = float(x_min_str)
    x_max = float(x_max_str)
    funkcja = wspolczynnik_funkcji.strip()

    # Generowanie wartości x i y przy użyciu eval()
    x_val = np.linspace(x_min, x_max, 200)
    x = x_val
    y_val = eval(f"{funkcja} + x*0")

    # Rysowanie wykresu ale bez show()
    plt.figure() 
    plt.plot(x_val, y_val)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Wykres wielomianu z użyciem eval: {funkcja}')
    plt.grid(True)

    # Zwracanie wartości na granicach przedziału
    return y_val[0], y_val[-1]

# Funkcja rysująca wykres na podstawie SymPy i lambdify()
def rysuj_wielomian_sympy(wejscie):
    # Definicja symbolu i konwersja do funkcji numerycznej za pomocą SymPy
    wspolczynnik_funkcji, zakres = wejscie.split(',')
    x_min_str, x_max_str = zakres.strip().split()
    x_min = float(x_min_str)
    x_max = float(x_max_str)
    funkcja_str = wspolczynnik_funkcji.strip()
    x = symbols('x')
    wzor = sympify(funkcja_str)
    funkcja_numeryczna = lambdify(x, wzor, modules=['numpy'])

    # Generowanie wartości x i y przy użyciu funkcji numerycznej
    x_val_sympy = np.linspace(x_min, x_max, 200)
    y_val_sympy = funkcja_numeryczna(x_val_sympy)

    # Rysowanie wykresu ale bez show()
    plt.figure() 
    plt.plot(x_val_sympy, y_val_sympy)
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.title(f'Wykres wialomianu z użyciem Sympy i lambdify : {funkcja_str}')
    plt.grid(True)

    # Zwracanie wartości na granicach przedziału
    return y_val_sympy[0], y_val_sympy[-1]

if __name__ == '__main__':
    # Przykładowe wywołanie pierwszej funkcji
    wejscie1 = "x**3 + 3*x + 1, -10 10"
    
    # Pierwszy wykres z eval
    wynik_eval = rysuj_wielomian(wejscie1)
    print("Wynik (eval):", wynik_eval)
    
    # Drugie wejście dla funkcji SymPy - bardziej złożona funkcja 
    wejscie2 = "x**4 - 5*x**2 + 3*sin(x), -10 10"  
    
    # Drugi wykres z SymPy
    wynik_sympy = rysuj_wielomian_sympy(wejscie2)
    print("Wynik (SymPy):", wynik_sympy)
    
    # Wyświetlanie obu wykresów
    plt.show()
