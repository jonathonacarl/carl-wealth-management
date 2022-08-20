# ============================================================================
#   Pull data, create chart
# ============================================================================
import pandas as pd
import os
import wrds
from fredapi import Fred
import yfinance as yf


def get_hist_sp(wrds):
    # sprtrn, vwretd, usdval
    crsp_query = """select caldt as date, spindx as sp, sprtrn, vwretd, usdval from crsp.dsp500p"""
    sp = wrds.raw_sql(crsp_query)
    return sp


def get_curr_sp(fred, min_date="2022-04-01"):
    fred = Fred(api_key="2f4b2a2f6b2401149c51f89021f47f49")
    sp = pd.DataFrame(fred.get_series("SP500"), columns=["sp"]).reset_index()
    sp = sp.rename(columns={"index": "date"})
    sp = sp[sp["date"] > min_date].reset_index(drop=True)
    return sp


def write_sp(sp):
    sp_all = pd.concat(sp).reset_index(drop=True)
    sp_all["date"] = pd.to_datetime(sp_all["date"])
    sp_all.to_csv("data/sp_backtesting.csv.gz", index=False)


def get_data():
    ticker_list = ["TQQQ", "SQQQ", "SPY", "UVXY", "^VIX", "^GSPC", "^DJI", "^IXIC"]
    tickers = [yf.Ticker(t) for t in ticker_list]
    data = [t.history(period="max") for t in tickers]
    [data[i].to_csv("data/" + ticker_list[i] + ".csv.gz") for i in range(len(data))]


def main():
    wrds_conn = wrds.Connection(wrds_username="mcarl")
    fred = Fred(api_key="2f4b2a2f6b2401149c51f89021f47f49")

    sp_hist = get_hist_sp(wrds_conn)
    sp_curr = get_curr_sp(fred, min_date=str(sp_hist["date"].max()))
    write_sp([sp_hist, sp_curr])

    get_data()


if __name__ == "__main__":
    main()
