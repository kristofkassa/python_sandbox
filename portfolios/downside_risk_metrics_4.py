import datetime

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt


# VaR - Historical Method

start = datetime.date(2016, 1, 1)
end = datetime.date(2021, 11, 28)
# end = datetime.date.today()
try:
    prices = web.DataReader(["BTC-USD"], "yahoo", start, end)["Adj Close"]
except:  # noqa E722
    # If there are connectivity issues, use backup data
    prices = pd.read_pickle("data/btc-usd.pkl")

returns = prices.pct_change()
returns = returns.rename(columns={"BTC-USD": "Bitcoin"})
returns = returns.dropna()

sns.histplot(data=returns)

plt.show()


def getHistoricalVar(returns, confidenceLevel):
    var = 100 * np.percentile(returns, 100 - confidenceLevel)
    print(
        "With %.2f%% percent confidence, we can say the most our portfolio will lose in a day is %.3f%% using "
        "historical VaR "
        % (confidenceLevel, var)
    )


getHistoricalVar(returns.Bitcoin, 95)

getHistoricalVar(returns.Bitcoin, 99)

# Conditional Value at Risk - CVaR


def getHistoricalCVar(returns, confidenceLevel):
    var = np.percentile(returns, 100 - confidenceLevel)
    cvar = returns[returns <= var].mean()
    print(
        "With %.2f%% percent confidence VaR, our Expected Shortfall is %.2f%% using historical VaR"
        % (confidenceLevel, 100 * cvar)
    )


getHistoricalCVar(returns.Bitcoin, 95)

start = datetime.date(2016, 1, 1)
end = datetime.date(2021, 11, 28)
# end = datetime.date.today()
prices = web.DataReader(["BLV"], "yahoo", start, end)["Adj Close"]
returns = prices.pct_change()
returns = returns.dropna()

getHistoricalVar(returns.BLV, 95)

getHistoricalCVar(returns.BLV, 95)

# Parametric Method

# Parametric Method with Normal Distribution

start = datetime.date(2010, 1, 1)
end = datetime.date(2021, 11, 28)
# end = datetime.date.today()
prices = web.DataReader(["AAPL"], "yahoo", start, end)["Adj Close"]
returns = prices.pct_change()
returns = returns.dropna()

mean = returns.AAPL.mean()
std = returns.AAPL.std()

print("Parametric VaR: %.2f%%" % (100 * stats.norm.ppf(0.05, mean, std)).round(3))
getHistoricalVar(returns.AAPL, 95)

# Parametric Method with T-distribution

# degrees of freedom
dof = 4
tVaR = np.sqrt((dof - 2) / dof) * stats.t.ppf(0.05, dof) * std - mean
(100 * tVaR).round(3)

# Monte Carlo Simulation This method runs a series of simulations, usually in the thousands, where each return stream
# is represented as a random variable. This variable can be taken from any probability distribution, which is great
# because that means it doesn’t necessarily assume the normal distribution. There is a lot of flexibility in choosing
# what kind of distribution to use. All the variables are then dollar-weighted and simulated to see what the total
# portfolio value is at the end of each run. These simulation returns are then sorted lowest to highest, and we can
# easily look to see what the Value at Risk is using similar computations to the historical method, except this time,
# we’re using simulated returns instead of historical returns. For example, if you ran a series of 1,000 simulations,
# you would look at the 50th lowest value to determine the VaR for a 95% confidence interval.
#
# Considerations for this method:
#
# Estimations will not be effective if the probability distributions used to determine the random variables are
# incorrect. Many use past data to get an idea of what the probability distribution should be; this method at least
# allows some subjectivity to doing this. You can estimate VaR more effectively for portfolios containing options
# with this method versus the parametric method since Monte Carlo doesn’t assume a normal distribution of returns. 6.
# Conclusion