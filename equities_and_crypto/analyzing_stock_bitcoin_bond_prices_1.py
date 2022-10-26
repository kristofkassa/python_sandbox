# Analyzing Prices of Stocks, Bitcoin, and Bonds

import datetime

import numpy as np
import pandas_datareader.data as web
from matplotlib import pyplot as plt


def main():
    # start = datetime.date.today() - datetime.timedelta(days=5*365)
    # end = datetime.date.today()
    start = datetime.date(2016, 11, 16)
    end = datetime.date(2021, 11, 18)
    df = web.DataReader(["AMZN", "TSLA", "BTC-USD"], "yahoo", start='2012-11-16', end='2022-8-20')["Adj Close"]

    df = df.join(web.DataReader(["BLV"], "yahoo", start, end)["Adj Close"])

    # df["2015-01-01":"2021-12-31"].plot()

    # Show plot
    # plt.show()

    # Calculate log returns, remove unused columns, drop nulls

    df = df.dropna()
    df["Amazon"] = np.log(df.AMZN) - np.log(df.AMZN.shift(1))
    df["Tesla"] = np.log(df.TSLA) - np.log(df.TSLA.shift(1))
    df["Bitcoin"] = np.log(df["BTC-USD"]) - np.log(df["BTC-USD"].shift(1))
    df = df.iloc[1:, 5:]

    # Volatility in one plot
    # df["2018-01-01":"2021-12-31"].plot()

    # Volatility separated
    ax1 = df.plot(figsize=(15, 3), y="Tesla", title='Tesla Daily Returns')
    ax2 = df.plot(figsize=(15, 3), y="Bitcoin", title='Bitcoin Daily Returns')

    ax1.set_ylim(-0.5, 0.4)
    ax2.set_ylim(-0.5, 0.4)
    # Show plot
    plt.show()

    print(df.describe())

    print(((df[["Bitcoin", "Tesla"]].mean() + 1).pow(365) - 1) * 100)

    # Most investors hold a mix of stocks/cryptocurrencies and bonds. A rule of thumb that’s commonly used to
    # determine this mix is to subtract your age from 100; the resulting number is the percentage of assets that
    # should be in risky assets, like stocks. In other words, a 26-year-old should be putting (100-26) = 74% of their
    # assets in stocks and 26% in bonds.


if __name__ == '__main__':
    main()
