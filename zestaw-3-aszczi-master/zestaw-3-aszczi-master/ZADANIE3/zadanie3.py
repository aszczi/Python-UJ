import yfinance as yf
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

def find_crossovers():
    """
    Pobierz dane BTC-USD od 2024-01-01 do 2025-11-20, oblicz 50-dniowa i 200-dniowa srednia kroczaca, 
    zidentyfikuj punkty przeciecia i zwroc liste dat tych przeciec.
    
    Returns:
        list: Lista dat przeciec w formacie 'YYYY-MM-DD'.
    """
    data = yf.download('BTC-USD', start='2024-01-01', end='2025-11-20', auto_adjust=False, progress=False)

    if isinstance(data.columns, pd.MultiIndex):
        try:
            data = data.xs('BTC-USD', level='Ticker', axis=1)
        except KeyError:
            pass #Fallback

    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    data['Diff'] = data['MA50'] - data['MA200']

    crossovers = data[
        (data['Diff'] * data['Diff'].shift(1) < 0) & 
        (data['MA200'].notna())
    ]

    crossover_dates = crossovers.index.strftime('%Y-%m-%d').tolist()

    return crossover_dates #lista



def calculate_total_btc_traded():
    """
    Pobierrz dane BTC-USD z okresu 2024-01-01 do 2025-11-20, oblicz liczbe BTC handlowanych w kaÅ¼dym dniu
    oraz zwroc liczbe BTC dla dnia z najwyÅ¼szym wolumenem.
    
    Returns:
        int: liczba BTC handlowanych w dniu z najwyz¼szym wolumene
    """
    data = yf.download('BTC-USD', start='2024-01-01', end='2025-11-20', auto_adjust=False, progress=False)
    
    if isinstance(data.columns, pd.MultiIndex):
        try:
            data = data.xs('BTC-USD', level='Ticker', axis=1)
        except KeyError:
            pass

    btc_volume = data['Volume'] / data['Close']

    max_btc_volume = btc_volume.max()
    return int(max_btc_volume) # int


if __name__ == '__main__':
    crossover_dates = find_crossovers()
    total_traded = calculate_total_btc_traded()

    print(" ".join(crossover_dates))
    print(total_traded)
    
    #Wykres :)
    #btc_data = yf.download('BTC-USD', start='2024-01-01', end='2025-11-20', auto_adjust=False, progress=False)
    #btc_data['50-day MA'] = btc_data['Close'].rolling(window=50).mean()
    #btc_data['200-day MA'] = btc_data['Close'].rolling(window=200).mean()

    #plt.plot(btc_data.index, btc_data['Close'], label='BTC-USD Close Price')
    #plt.plot(btc_data.index, btc_data['50-day MA'], label='50-Day Moving Average', linestyle='--')
    #plt.plot(btc_data.index, btc_data['200-day MA'], label='200-Day Moving Average', linestyle='--')
    #plt.title('BTC-USD with 50-Day and 200-Day Moving Averages')
    #plt.xlabel('Date')
    #plt.ylabel('Price (USD)')
    #plt.legend()
    #plt.grid(True, alpha=0.3)
