import pandas as pd
import os
import matplotlib.pyplot as plt
from ta.volatility import BollingerBands
from ta.utils import dropna

os.chdir("/Users/matthewcarl/Dropbox/CWM/carl-wealth-management")

def read_data(series='sp'):
    data = pd.read_csv('data/' + series + '.csv.gz', engine='c')
    return data

def get_tech_ind(data, var="sp"):

    data = dropna(data)

    """
        Bollinger Bands
            MB = SUM(n last close values) / n
            UB = MB + (X * StdDev)
            LB = MB — (X * StdDev)
    """
    indicator_bb = BollingerBands(close=data[var], window=20, window_dev=2)
    data[var+'_bbm'] = indicator_bb.bollinger_mavg()
    data[var+'_bbh'] = indicator_bb.bollinger_hband()
    data[var+'_bbl'] = indicator_bb.bollinger_lband()

    """
        Moving Average Convergence Divergence
            MACD = EMA(n1, close) — EMA(n2, close)
            MACD_Signal = EMA(n3, MACD)
            MACD_Difference = MACD — MACD_Signal
    """
    return data

def make_chart(data_plt, var="price", xlab="Date", start_date="2020-01-01"):
    data_plt = data_plt[data_plt['date'] >= start_date]
    fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
    ax.plot(pd.to_datetime(data_plt['date']), data_plt[var], color='black')
    ax.plot(pd.to_datetime(data_plt['date']),
            data_plt[var+'_bbm'], color='blue', alpha=0.8, linestyle='dotted')
    ax.plot(pd.to_datetime(data_plt['date']),
            data_plt[var+'_bbh'], color='red', alpha=0.8, linestyle='dotted')
    ax.plot(pd.to_datetime(data_plt['date']),
            data_plt[var+'_bbl'], color='red', alpha=0.8, linestyle='dotted')
    ax.set_xlabel(xlab)
    fig.savefig('charts/' + var + ".pdf")

def execute_chart(chart='sp'):
    data = read_data(series=chart)
    plt_data = get_tech_ind(data, chart)
    make_chart(plt_data, var = chart, xlab="Date")

def main():
    charts = ['sp', 'vix']
    [execute_chart(chart) for chart in charts]

if __name__ == '__main__':
    main()
