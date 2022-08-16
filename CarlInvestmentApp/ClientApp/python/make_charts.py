import pandas as pd
import os
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import mplfinance as fplt
import io
from ta.momentum import KAMAIndicator

os.chdir("/Users/matthewcarl/Dropbox/CWM/carl-wealth-management")


def read_data(series='TQQQ'):
    data = pd.read_csv('data/' + series + '.csv.gz', engine='c')
    data['Date'] = pd.to_datetime(data['Date'])
    return data


def get_tech_ind(data):
    # data = dropna(data)
    data['KAMA_3'] = KAMAIndicator(
        data['Close'], window=3, pow1=2, pow2=30).kama()
    data['KAMA_20'] = KAMAIndicator(
        data['Close'], window=20, pow1=2, pow2=30).kama()
    return data

def make_chart(data_plt, series="TQQQ", type="DAILY_YTD"):
    if type == "DAILY_YTD":
        start_date = pd.to_datetime(str(data_plt['Date'].max().year))
    elif type=="WEEKLY_YTD":
        start_date = pd.to_datetime(str(data_plt['Date'].max().year))
        wclose = data_plt.groupby([data_plt['Date'].dt.year, data_plt['Date'].dt.week],
            as_index=False)[['Date', 'Close']].last()
        wopen = data_plt.groupby([data_plt['Date'].dt.year, data_plt['Date'].dt.week],
            as_index=False)['Open'].first()
        whigh = data_plt.groupby([data_plt['Date'].dt.year, data_plt['Date'].dt.week],
            as_index=False)['High'].max()
        wlow = data_plt.groupby([data_plt['Date'].dt.year, data_plt['Date'].dt.week],
            as_index=False)['Low'].min()
        wvol = data_plt.groupby([data_plt['Date'].dt.year, data_plt['Date'].dt.week],
            as_index=False)['Volume'].sum()
        data_plt = pd.concat([wclose,wopen,whigh,wlow,wvol], axis=1)
    elif type == "DAILY_MONTH":
        start_date = data_plt['Date'].max() - relativedelta(months=1)
    elif type == "DAILY_WEEK":
        start_date = data_plt['Date'].max() - relativedelta(days=7)

    data_plt = get_tech_ind(data_plt)
    data_plt = data_plt[data_plt['Date'] >= start_date]
    data_plt = data_plt.set_index('Date')
    
    kama = [fplt.make_addplot(data_plt["KAMA_3"], linestyle='dotted', color='blue'),
            fplt.make_addplot(data_plt["KAMA_20"], linestyle='dotted', color='black')]
    fplt.plot(data_plt[["Open", "High", "Low", "Close", "Volume"]], type='candle', volume=True,
              style='yahoo', addplot=kama, tight_layout=True, savefig="../public/images/"+type+"_"+series+".png")
    
def execute_chart(chart='TQQQ'):
    data = read_data(series=chart)
    make_chart(data, series=chart, type='DAILY_YTD')
    make_chart(data, series=chart, type='WEEKLY_YTD')
    make_chart(data, series=chart, type='DAILY_MONTH')
    make_chart(data, series=chart, type='DAILY_WEEK')


def main():
    charts = ['TQQQ', 'SQQQ', 'SPY', 'UVXY', "^VIX", "^GSPC", "^DJI", "^IXIC"]
    [execute_chart(chart) for chart in charts]

if __name__ == '__main__':
    main()
