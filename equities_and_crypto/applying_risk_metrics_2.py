import numpy as np
import pandas as pd
import pandas_datareader.data as web

pd.options.display.float_format = "{:,.3f}".format
import datetime
from datetime import date

import seaborn as sns
from matplotlib import pyplot as plt

# Pull 10 years daily price data for S&P 500 and Russel 2000

# start = datetime.date.today()-datetime.timedelta(365*10)
# end = datetime.date.today()
start = datetime.date(2011, 11, 25)
end = datetime.date(2021, 11, 22)

prices = web.DataReader(["^GSPC", "^RUT"], "yahoo", start, end)["Adj Close"]

# Rename column to make names more intuitive
prices = prices.rename(columns={"^GSPC": "SP500", "^RUT": "Russell2000"})

print(prices.describe())

print(prices.tail())

# Calculate log returns
df = np.log(prices) - np.log(prices.shift(1))
df = df.iloc[1:, 0:]

print(df.head())

print(df.mean() * 100)

# Volatility of last year

currYear = prices.loc[
           date.today() - datetime.timedelta(365): date.today()  # noqa E203
           ]

print((currYear.max() - currYear.min()) / prices.iloc[-1])

# Moving Averages

prices["SP500 50 day_rolling_avg"] = prices.SP500.rolling(50).mean()

# set figure size
plt.figure(figsize=(12, 5))

# plot a simple time series plot
# using seaborn.lineplot()
sns.lineplot(x="Date", y="SP500", data=prices, label="Daily S&P 500 Prices")

# plot using rolling average
sns.lineplot(x="Date", y="SP500 50 day_rolling_avg", data=prices, label="Rollingavg")

# plt.show()

# Standard Deviation
print(df.std())


def investCompare(startTime, endTime, tickers):
    # pull price data from yahoo -- (list(tickers.keys())) = ['^GSPC','^RUT']
    prices = web.DataReader(list(tickers.keys()), "yahoo", startTime, endTime)[
        "Adj Close"
    ]
    prices = prices.rename(columns=tickers)
    returns = np.log(prices) - np.log(prices.shift(1))
    returns = returns.iloc[1:, 0:]

    # pull data into separate DataFrame, 52weeks to just look at the last 365 days of data for calculating our high/low metric
    currYear = prices.loc[
               date.today() - datetime.timedelta(365): date.today()  # noqa E203
               ]
    highLow = (currYear.max() - currYear.min()) / prices.iloc[-1]
    highLow = pd.DataFrame(highLow, columns=["HighMinusLow"])

    # Moving average volatility
    MA = pd.DataFrame(
        ((abs(prices - prices.rolling(50).mean())) / prices).mean(),
        columns=["MovingAverageVolatility"],
    )

    investments = pd.merge(highLow, MA, on="Symbols")
    investments = pd.merge(
        investments,
        pd.DataFrame(returns.std(), columns=["StandardDeviation"]),
        on="Symbols",
    )
    investments = pd.merge(
        investments,
        pd.DataFrame(100 * returns.mean(), columns=["Daily Return Percentage"]),
        on="Symbols",
    )

    return investments.round(3)


comparison = investCompare(
    datetime.date(2020, 1, 1),
    datetime.date.today(),
    {"^GSPC": "SP500", "^RUT": "Russell2000", "AAPL": "Apple"},
)

print(comparison)


# Domestic vs Foreign stocks
comparison2 = investCompare(
    datetime.date(2010, 1, 1),
    datetime.date.today(),
    {"^GSPC": "SP500", "SPEU": "Europe ETF", "GXC": "China ETF"},
)

print(comparison2)
