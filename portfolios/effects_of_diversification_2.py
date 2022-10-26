import datetime

import pandas as pd
import pandas_datareader.data as web
import seaborn as sns
from matplotlib import pyplot as plt

start = datetime.date(2016, 11, 29)
end = datetime.date(2021, 11, 28)
# start = datetime.date.today()-datetime.timedelta(365*10)
# end = datetime.date.today()
prices = web.DataReader(["JPM", "BTC-USD"], "yahoo", start, end)["Adj Close"]
prices = prices.rename(columns={"BTC-USD": "BTC"})
prices = prices.dropna()
returns = prices.pct_change()

# observe data
returns.head()

# Determine weights
initialJPM = prices.JPM[0] * 100
initialBTC = prices.BTC[0] * 5
initialInvestment = initialJPM + initialBTC

weightJPM = initialJPM / (initialBTC + initialJPM)
weightBTC = 1 - weightJPM
print(
    "This would make the weights %.3f and %.3f for JPM and BTC respectively"
    % (weightJPM, weightBTC)
)

returns["Portfolio"] = (returns.JPM * weightJPM) + (returns.BTC * weightBTC)
returns = returns + 1
returns.head()

returns.iloc[0] = 10000
returns.head()

portValues = returns.cumprod()
portValues["Date"] = portValues.index

sns.lineplot(x="Date", y="value", hue="Symbols", data=portValues.melt(id_vars=["Date"]));
plt.show()

# Quantifying Diversification Benefits

returns.drop(index=returns.index[0], axis=0, inplace=True)
returns = returns - 1
returns.head()

returns.std().round(3)


# Covariance-Correlation relationship


def getReturns(startTime, endTime, tickers):
    # pull price data from yahoo -- (list(tickers.keys())) = ['^GSPC','^RUT']
    prices = web.DataReader(list(tickers.keys()), "yahoo", startTime, endTime)[
        "Adj Close"
    ]
    prices = prices.rename(columns=tickers)
    prices = prices.dropna()
    return prices.pct_change()


res = getReturns(
    datetime.date(2016, 11, 29),
    datetime.date(2021, 11, 28),
    {"JPM": "JPM", "BTC-USD": "Bitcoin"},
)

print(res.head())

correlation = getReturns(
    datetime.date(2016, 11, 29),
    datetime.date(2021, 11, 28),
    {"JPM": "JPM", "BTC-USD": "Bitcoin", "BLV": "BLV"},
).corr()

print(correlation)


def compareVariance(startTime, endTime, tickers, weights):
    returns = getReturns(startTime, endTime, tickers)
    tmp = weights * returns
    returns["Portfolio"] = tmp[tmp.columns[0]] + tmp[tmp.columns[1]]
    standardDev = returns.std()
    avgReturns = returns.mean()
    res = pd.concat([avgReturns * 100, standardDev], axis=1)
    res.columns = ["Daily Average Return Percentage", "Standard Deviation of Returns"]
    return res.round(3)


compareVariance(
    datetime.date(2016, 11, 29),
    datetime.date(2021, 11, 28),
    {"JPM": "JPM", "BTC-USD": "Bitcoin"},
    [0.652, 0.348],
)

compareVariance(
    datetime.date(2016, 11, 29),
    datetime.date(2021, 11, 28),
    {"JPM": "JPM", "BTC-USD": "Bitcoin"},
    [0.8, 0.2],
)

getReturns(
    datetime.date(2016, 11, 29),
    datetime.date(2021, 11, 28),
    {"JPM": "JPM", "F": "F", "GM": "GM"},
).mean()

getReturns(
    datetime.date(2016, 11, 29),
    datetime.date(2021, 11, 28),
    {"JPM": "JPM", "F": "F", "GM": "GM"},
).corr()

compareVariance(
    datetime.date(2016, 11, 29),
    datetime.date(2021, 11, 28),
    {"F": "F", "GM": "GM"},
    [0.5, 0.5],
)

compareVariance(
    datetime.date(2016, 11, 29),
    datetime.date(2021, 11, 28),
    {"F": "F", "JPM": "JPM"},
    [0.5, 0.5],
)