# Working With Securities Datas

# -------------- 1 --------------
# Using the `pandas_datareader` package, we'll get Netflix stock information from Yahoo Finance
import pandas_datareader as pdr

# Request data via Yahoo public API
data = pdr.get_data_yahoo("NFLX")
# Display Info
print(data.info())

# -------------- 2 --------------
# If we wanted 1 day's worth of Bitcoin data, we can use the following
import yfinance as yf

BTC = yf.Ticker("BTC-USD")
BtcData = BTC.history(period="5D")
print(BtcData.tail(2))

# -------------- 3 --------------
# The FX market is open 24 hours a day, 5 days a week.
# Let's get the most recent FX data: Japanese Yen to Eurodollars

data = yf.download(tickers="JPYAUD=X", period="1d", interval="15m")
data

# Let's look at a few fundamentals on Uber.
ticker = "UBER"
UberFundamentals = yf.Ticker(ticker)
print(UberFundamentals.info.keys())
print(UberFundamentals.info["freeCashflow"])
print(UberFundamentals.info["priceToBook"])