#============================================================================
#   Pull data, create chart
#============================================================================
import pandas as pd
import os
import wrds
from fredapi import Fred

os.chdir("/Users/matthewcarl/Dropbox/CWM/carl-wealth-management") # Personal
# os.chdir('/project6/mcarl')  # Linstat


def get_hist_sp(wrds):
    # sprtrn, vwretd, usdval
    crsp_query = """select caldt as date, spindx as sp, sprtrn, vwretd, usdval from crsp.dsp500p"""
    sp = wrds.raw_sql(crsp_query)
    return sp


def get_curr_sp(fred, min_date="2022-04-01"):
    fred = Fred(api_key='2f4b2a2f6b2401149c51f89021f47f49')
    sp = pd.DataFrame(fred.get_series("SP500"), columns=['sp']).reset_index()
    sp = sp.rename(columns={'index':'date'})
    sp = sp[sp['date']>min_date].reset_index(drop=True)
    return sp


def write_sp(sp):
    sp_all = pd.concat(sp).reset_index(drop=True)
    sp_all['date'] = pd.to_datetime(sp_all['date'])
    sp_all.to_csv('data/sp.csv.gz', index=False)


def get_vix(fred):
    vix = pd.DataFrame(fred.get_series("VIXCLS"), columns=['vix']).reset_index()
    vix = vix.rename(columns={'index':'date'})
    vix.to_csv('data/vix.csv.gz', index=False)


def get_etf_query_list():
    dates = pd.bdate_range(start="2010-12-02", end="2021-12-31")
    table_query_list = ['ctm_' + str(x)[0:10].replace('-', '') for x in dates]
    tck_query_list = """'TQQQ', 'SQQQ'"""
    taq_query_list = ["""select sym_root, date, time_m, price from taqmsec.""" + table_query_list[i] +
                      """ where time_m > '15:55:00.000000' and time_m < '16:00:00.000000'""" +
                      """ and tr_corr = '00' and sym_root in (""" +
                      tck_query_list + """)"""
                      for i in range(len(table_query_list))]
    return taq_query_list


def get_etf(wrds, taq_query):
    try:
        etf = wrds.raw_sql(taq_query, date_cols=[
                           'date']).reset_index(drop=True)
        etf = etf.groupby(['sym_root','date'])['price'].last().T.reset_index()
        etf = pd.pivot(etf, index='date', columns='sym_root', values='price').reset_index()
    except:
        etf=pd.DataFrame()

    print("FINISHED ", taq_query)
    return etf


def write_etf(etf_data_list):
    etf_all = pd.concat(etf_data_list).reset_index(drop=True)
    etf_all.to_csv('data/etf.csv.gz', index=False)


def main():
    wrds = wrds.Connection(wrds_username='yangliu5')
    fred = Fred(api_key='2f4b2a2f6b2401149c51f89021f47f49')
    
    sp_hist = get_hist_sp(wrds)
    sp_curr = get_curr_sp(fred, min_date=str(sp_hist['date'].max()))
    write_sp([sp_hist, sp_curr])

    get_vix(fred)

    etf_query_list = get_etf_query_list()
    etf_data_list = [get_etf(wrds, query) for query in etf_query_list]
    write_etf(etf_data_list)


if __name__ == '__main__':
    main()
