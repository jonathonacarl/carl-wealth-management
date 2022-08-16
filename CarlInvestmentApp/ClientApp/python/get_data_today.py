import pandas as pd
import os
import gzip
import yfinance as yf


os.chdir("/Users/matthewcarl/Dropbox/CWM/carl-wealth-management")  # Personal

def get_data_today():
    ticker_list = ['TQQQ', 'SQQQ', 'SPY',
                   'UVXY', "^VIX", "^GSPC", "^DJI", "^IXIC"]
    tickers = [yf.Ticker(t) for t in ticker_list]
    data = [t.history(period='1d') for t in tickers]
    [data[i].to_csv('data/'+ticker_list[i]+'.csv.gz', mode='a', header=False)
        for i in range(len(data))]

def main():
    get_data_today()


if __name__ == '__main__':
    main()
