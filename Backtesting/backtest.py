import yfinance as yf
import talib
import pandas as pd
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
tcs = yf.Ticker("TCS.NS")
df = tcs.history(period="1y", interval="1d")
df["MA_200"] = talib.MA(df["Close"], timeperiod=22)
print(df)
for i in df.index[22:]:
    print(i)

