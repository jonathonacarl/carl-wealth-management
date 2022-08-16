import pandas as pd
import numpy as np
import ta

def backtest_cwm(series="TQQQ"):
    data = pd.read_csv("data/"+series+".csv.gz")
    data['KAMA_3'] = ta.momentum.KAMAIndicator(
        data['Close'],window=3, pow1=2, pow2=30).kama()
    data['KAMA_20'] = ta.momentum.KAMAIndicator(
        data['Close'], window=20, pow1=2, pow2=30).kama()
    data['d_KAMA_3'] = data['KAMA_3'] - data['KAMA_3'].shift(1)
    data = data.dropna()

    data.loc[(data['Close'] > data['KAMA_3']) \
             & (data['KAMA_3'] > data['KAMA_20'])\
             & (data['d_KAMA_3'] > 0), 'bull_entry'] = 1
    data.loc[(data['d_KAMA_3'] > 0)\
             & (data['KAMA_3'] < data['KAMA_20']), 'bear_entry'] = 1

def backtest_mkt():
    pass

def main():
    backtest_cwm()
    backtest_mkt()

if __name__ == '__main__':
    main()
