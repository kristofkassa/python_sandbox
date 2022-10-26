import datetime

import matplotlib.pyplot as plt
import pandas_datareader.data as web
import seaborn as sns

start = datetime.date(2006, 1, 1)
end = datetime.date(2021, 11, 28)
# end = datetime.date.today()
prices = web.DataReader(["XLF"], "yahoo", start, end)["Adj Close"]
prices = prices.dropna()

# set figure size
plt.figure(figsize=(12, 5))

# plot a simple time series plot
# using seaborn.lineplot()
sns.lineplot(x="Date", y="XLF", data=prices, label="Daily XLF 500 Prices")

drawdown = (
    prices["2006-01-01":"2010-01-01"].min() - prices["2006-01-01":"2010-01-01"].max()
) / prices["2006-01-01":"2010-01-01"].max()

print(100 * drawdown.round(3))
