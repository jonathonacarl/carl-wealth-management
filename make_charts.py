import pandas as pd
import os
from dateutil.relativedelta import relativedelta
from ta.volatility import BollingerBands
from ta.utils import dropna
import matplotlib.pyplot as plt
import io
# from mplfinance.original_flavor import graph_candlestick
import mplfinance as fplt

os.chdir("/Users/matthewcarl/Dropbox/CWM/carl-wealth-management")


def read_data(series='TQQQ'):
    data = pd.read_csv('data/' + series + '.csv.gz', engine='c')
    data['Date'] = pd.to_datetime(data['Date'])
    # data['Diff'] = data['Open'] - data['Close']
    # data['Colors'] = ['g' if v >= 0 else 'r' for v in data['Diff']]
    return data


def get_tech_ind(data):

    # data = dropna(data)

    """
        Bollinger Bands
            MB = SUM(n last close values) / n
            UB = MB + (X * StdDev)
            LB = MB — (X * StdDev)
    """
    indicator_bb = BollingerBands(close=data['Close'], window=20, window_dev=2)
    data['Close_bbm'] = indicator_bb.bollinger_mavg()
    data['Close_bbh'] = indicator_bb.bollinger_hband()
    data['Close_bbl'] = indicator_bb.bollinger_lband()

    """
        Moving Average Convergence Divergence
            MACD = EMA(n1, close) — EMA(n2, close)
            MACD_Signal = EMA(n3, MACD)
            MACD_Difference = MACD — MACD_Signal
    """
    # data["macd"], data["macd_signal"], data["macd_hist"] = ta.MACD(data['Close'])
    return data

def make_chart(data_plt, series="TQQQ", type="DAILY_YTD"):
    if type == "DAILY_YTD":
        start_date = pd.to_datetime(str(data_plt['Date'].max().year))
    elif type=="WEEKLY_YTD":
        start_date = pd.to_datetime(str(data_plt['Date'].max().year))
        data_plt.groupby(data_plt['Date'].dt.week, as_index=False).last()
    elif type == "DAILY_MONTH":
        start_date = data_plt['Date'].max() - relativedelta(months=1)
    elif type == "DAILY_WEEK":
        start_date = data_plt['Date'].max() - relativedelta(days=7)

    data_plt = data_plt[data_plt['Date'] >= start_date]
    data_plt = data_plt.set_index('Date')
    if type in ["DAILY_YTD", "WEEKLY_YTD"]:
        # bb = fplt.make_addplot(data_plt[["Close_bbm", "Close_bbh", "Close_bbl"]])
        fplt.plot(data_plt[["Open", "High", "Low", "Close", "Volume"]], volume=True, style='yahoo',
                type='renko', renko_params=dict(brick_size='atr', atr_length=2),
                savefig="charts/"+type+"_"+series+".png")
    elif type in ["DAILY_MONTH", "DAILY_WEEK"]:
        fplt.plot(data_plt[["Open", "High", "Low", "Close", "Volume"]], volume=True, style='yahoo',
                  type='candle', savefig="charts/"+type+"_"+series+".png")


def execute_chart(chart='TQQQ'):
    data = read_data(series=chart)
    data_plt = get_tech_ind(data)
    make_chart(data_plt, series=chart, type='DAILY_YTD')
    make_chart(data_plt, series=chart, type='WEEKLY_YTD')
    make_chart(data_plt, series=chart, type='DAILY_MONTH')
    make_chart(data_plt, series=chart, type='DAILY_WEEK')
    

def main():
    charts = ['TQQQ', 'SQQQ', 'SPY', 'UVXY', "^VIX", "^GSPC", "^DJI", "^IXIC"]
    [execute_chart(chart) for chart in charts]

if __name__ == '__main__':
    main()
