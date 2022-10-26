# Financial Data Best Practices

import yfinance as yf
import pandas_datareader as pdr  # access fred

# -------------- 1 --------------
# extract api key: put your key in between the angle brackets <>
myKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
fred_api_key = "<ENTER YOUR API KEY HERE>"


# Using code from FRED API: Get US Economic Data using Python
def get_fred_data(param_list, start_date, end_date):
    df = pdr.DataReader(param_list, "fred", start_date, end_date)
    return df.reset_index()


# Let's see what the Fed Funds rate was since 2000
series = "FEDFUNDS"
# get data for series
df = get_fred_data(param_list=[series], start_date="2000-01-01", end_date="2022-05-03")
print(df)

# -------------- 2 --------------
data = yf.download(tickers="NFLX", period="1d", interval="5m")
print(data)
