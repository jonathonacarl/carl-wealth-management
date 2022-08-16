import pandas as pd
import io
import matplotlib.pyplot as plt
import mplfinance as fplt
from ta.momentum import KAMAIndicator
from ta.volatility import BollingerBands
from ta.utils import dropna
# from mplfinance.original_flavor import graph_candlestick
data = []
data_plt = []
series = ""

"""
---------------------------------------------------------
      INDICATORS
---------------------------------------------------------
"""
"""
      KAMA
"""
data['KAMA_3'] = KAMAIndicator(
    data['Close'], window=3, pow1=2, pow2=30).kama()
data['KAMA_20'] = KAMAIndicator(
    data['Close'], window=20, pow1=2, pow2=30).kama()


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
---------------------------------------------------------
      CHARTS
---------------------------------------------------------
"""

# Adding colors (not needed in fplt)
data_plt['Diff'] = data_plt['Open'] - data_plt['Close']
data_plt['Colors'] = ['g' if v >= 0 else 'r' for v in data_plt['Diff']]

# Renko chart
fplt.plot(data_plt[["Open", "High", "Low", "Close", "Volume"]], volume=True, style='yahoo',
        type='renko', renko_params=dict(brick_size='atr', atr_length=2),
        savefig="charts/"+type+"_"+series+".png")

# Chart with overlaid Bollinger Bands
bb = [fplt.make_addplot(data_plt["Close_bbm"], linestyle='dotted', color='blue'),
      fplt.make_addplot(data_plt["Close_bbh"], linestyle='dotted', color='black'), 
      fplt.make_addplot(data_plt["Close_bbl"], linestyle='dotted', color='black')]
fplt.plot(data_plt[["Open", "High", "Low", "Close", "Volume"]], volume=True, style='yahoo',
            type='candle', addplot=bb, savefig="charts/"+type+"_"+series+".png")

# Alternative options for scaling.
# See also discussions here: https://stackoverflow.com/questions/69199380/changing-margin-on-mplfinance-plot-when-savefig
fig, _ = plt.subplots(figsize=(8, 6), dpi=100)
fig, _ = fplt.plot(data_plt[["Open", "High", "Low", "Close", "Volume"]],
                   volume=True, style='yahoo', type='candle', addplot=kama,
                   scale_padding=0.5, returnfig=True)
fig.savefig("charts/"+type+"_"+series+".png")
