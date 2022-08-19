import pandas as pd
import numpy as np
import ta

def get_strat_kama(data):
    data["KAMA_3"] = ta.momentum.KAMAIndicator(
        data["Close"], window=3, pow1=2, pow2=30
    ).kama()
    data["KAMA_20"] = ta.momentum.KAMAIndicator(
        data["Close"], window=20, pow1=2, pow2=30
    ).kama()
    data["d_KAMA_3"] = data["KAMA_3"] - data["KAMA_3"].shift(1)
    data = data.dropna()

    data.loc[
        (data["Close"] > data["KAMA_3"])
        & (data["KAMA_3"] > data["KAMA_20"])
        & (data["d_KAMA_3"] > 0),
        "bull_entry",
    ] = 1
    data.loc[
        (data["KAMA_3"] < data["KAMA_20"])
        & (data["d_KAMA_3"] < 0)
        & (data["High"] < data["Close"].shift(1)),
        "bull_exit"
    ] = 1
    data.loc[
        (data["d_KAMA_3"] > 0) & 
        (data["KAMA_3"] < data["KAMA_20"]), 
        "bear_entry"
    ] = 1

    data.loc[data['bull_entry'] == 1,
             'entry_date'] = data.loc[data['bull_entry'] == 1, 'Date']
    data.loc[data['bull_exit'] == 1,
             'exit_date'] = data.loc[data['bull_exit'] == 1, 'Date']
    entries = data['entry_date'].dropna().reset_index(drop=True)
    exits = data['exit_date'].dropna().reset_index(drop=True)

    return entries, exits
 

def get_strat_returns(data, entries, exits):
    """
    Consider entry vector n and exit vector x
        n = (1,3,4,9,10)
        x = (5,7,11)

            1   2   3   4   5   6   7   8   9   10  11
        N   1       1   1                   1   1
        X                   1       1               1  

    We want a program that return the 2 pairs of entry/exit times:
        (1,5)
        (9,11)
    """
    start_trade = [entries[0]]
    end_trade = [exits[0]]
    for i in range(len(entries)):
        if ((entries[i] > start_trade[-1])) & (entries[i] < end_trade[-1]):
            pass
        elif (entries[i] < np.max(exits)):
            end_trade.append([e for e in exits if (
                e > entries[i])][0])
            start_trade.append(entries[i])
        else:
            start_trade.append([s for s in entries if (
                s > np.max(exits))][0])
            end_trade.append(np.max(data['Date']))
            break
    
    data_strat = pd.DataFrame([start_trade,end_trade]).T
    data_strat = data_strat.drop_duplicates().reset_index(drop=True)
    data_strat.columns = ["Date_Buy", "Date_Sell"]
    
    close = data[['Date','Close']]
    close.columns = ['Date_Buy', 'Close_Buy']
    data_strat = pd.merge(data_strat,close)
    close.columns = ['Date_Sell', 'Close_Sell']
    data_strat = pd.merge(data_strat, close)
    data_strat['Return'] = np.log(data_strat['Close_Buy']) - np.log(data_strat['Close_Sell'])
    return data_strat


def backtest_strat(series="TQQQ",
                   strategy = "KAMA",
                   investment = 10000,
                   start_date="1990-01-01",
                   end_date=pd.to_datetime("today")):
    data = pd.read_csv("data/" + series + ".csv.gz")

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    data['Date'] = pd.to_datetime(data['Date'])
    
    date_min = data['Date'].max()
    date_max = data['Date'].min()

    if ((start_date < date_min) | (end_date > date_max)):
        error = "For " + series + ", please specify a start and end \
                date between " + date_min + " and " + date_max
        raise ValueError(error)

    if strategy=="KAMA":
        entries, exits = get_strat_kama(data)
    else:
        error = "Please specify one of the following CWM strategies:\
                 KAMA ..."
        raise ValueError(error)

    
    data_strat = get_strat_returns(data, entries, exits)
    
    for r in data_strat['Return']:
        investment = investment*(1+r)
    
    return data_strat, investment
        

def backtest_mkt(index="^GSPC",
                 investment=10000,
                 start_date="1990-01-01",
                 end_date=pd.to_datetime("today")):
    if index not in ["^GSPC","^IXIC", "^DJI"]:
        error = "Please specify one of the following indices:\
                ^GSPC (S&P 500), ^IXIC (NASDAQ), or ^DJI (Dow Jones)"
        raise ValueError(error)

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    data['Date'] = pd.to_datetime(data['Date'])

    data = pd.read_csv("data/" + index + ".csv.gz")
    data['Return'] = np.log(data['Close']) - np.log(data['Close'].shift(1))
    data = data.dropna().reset_index(drop=True)

    data = data[(data['Date'] >= start_date)
                & (data['Date'] <= end_date)].reset_index(drop=True)

    tot_ret = data['Return'].sum()

    for r in data['Return']:
        investment = investment*(1+r)

    return investment, tot_ret



def main():
    data_strat, investment =\
        backtest_strat(series="TQQQ",
                       investment=10000,
                       start_date="1990-01-01",
                       end_date=pd.to_datetime("today"))
    investment, tot_ret =\
        backtest_mkt(index="^GSPC",
                     investment=10000,
                     start_date="1990-01-01",
                     end_date=pd.to_datetime("today"))


if __name__ == "__main__":
    main()
