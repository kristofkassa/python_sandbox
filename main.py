# Analyzing Prices of Stocks, Bitcoin, and Bonds

import datetime

import numpy as np
import pandas_datareader.data as web
from IPython.display import VimeoVideo


def main():
    # start = datetime.date.today() - datetime.timedelta(days=5*365)
    # end = datetime.date.today()
    start = datetime.date(2016, 11, 16)
    end = datetime.date(2021, 11, 18)
    df = web.DataReader(["AMZN", "F", "BTC-USD"], "yahoo", start, end)["Adj Close"]

    print(df.head)


if __name__ == '__main__':
    main()
