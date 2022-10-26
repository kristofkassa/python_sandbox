import datetime
import math

import numpy as np
import pandas_datareader.data as web

# Portfolio Returns

# Individual stock
start = datetime.date.today() - datetime.timedelta(365 * 10)
end = datetime.date.today()
prices = web.DataReader(["GE"], "yahoo", start, end)["Adj Close"]
initialPrice = prices.GE[0]
finalPrice = prices.GE[-1]
cashReturn = (finalPrice - initialPrice) * 100
print(
    "With an initial investment of $%.2f, the cash return of this investment would be %.3f - %.3f * 100 = $%.3f"
    % (initialPrice * 100, finalPrice, initialPrice, cashReturn)
)

# Basket of Assets

# Define all initial variables
# start = datetime.date.today()-datetime.timedelta(365*5)
# end = datetime.date.today()
start = datetime.date(2016, 11, 29)
end = datetime.date(2021, 11, 28)
prices = web.DataReader(["META", "CMG"], "yahoo", start, end)["Adj Close"]
initialFB = prices.META[0]
initialCMG = prices.CMG[0]
finalFB = prices.META[-1]
finalCMG = prices.CMG[-1]
FBWeight = initialFB / (initialFB + initialCMG)
CMGWeight = initialCMG / (initialFB + initialCMG)

print(
    "We have an initial investment in FB of $%.2f and in CMG $%.2f"
    % (initialFB * 100, initialCMG * 100)
)

print(
    "This would make the weights %.2f and %.2f for FB and CMG respectively"
    % (FBWeight, CMGWeight)
)

returnFB = 100 * (finalFB - initialFB) / initialFB
returnCMG = 100 * (finalCMG - initialCMG) / initialCMG

print(
    "This return over this period for Facebook is %.2f%% and %.2f%% for Chipotle"
    % (returnFB, returnCMG)
)

print(
    "Multiplying these individual returns by their weights gives %.2f (FB) and %.2f (CMG)"
    % (returnFB * FBWeight, returnCMG * CMGWeight)
)

# Calculating Portfolio Variance

weights = np.array([0.23, 0.77])
returns = prices.pct_change()
covariance = 252 * returns.cov()

variance = np.dot(weights.T, np.dot(covariance, weights))

# Print the result
print(str(np.round(variance, 4) * 100) + "%")

returns.var() * 252

np.round(math.sqrt(variance) * 100, 2)

# Sharpe Ratio of Portfolio

# portfolio_return / portfolio_standard_dev

# Cryptocurrencies

# Define all initial variables
# start = datetime.date.today()-datetime.timedelta(365*5)
# end = datetime.date.today()
start = datetime.date(2016, 11, 29)
end = datetime.date(2021, 11, 28)
prices = web.DataReader(["BTC-USD", "ETH-USD"], "yahoo", start, end)["Adj Close"]
prices = prices.rename(columns={"BTC-USD": "Bitcoin", "ETH-USD": "Ethereum"})

initialBTC = 5 * prices.Bitcoin[0]
initialETH = 100 * prices.Ethereum[0]
finalBTC = 5 * prices.Bitcoin[-1]
finalETH = 100 * prices.Ethereum[-1]
BTCWeight = initialBTC / (initialBTC + initialETH)
ETHWeight = initialETH / (initialBTC + initialETH)

print(
    "This would make the weights %.2f and %.2f for Bitcoin and Ethereum respectively"
    % (BTCWeight, ETHWeight)
)

returnBTC = 100 * (finalBTC - initialBTC) / initialBTC
returnETH = 100 * (finalETH - initialETH) / initialETH

np.round(returnBTC, 3)

np.round(returnETH, 3)

np.round(returnBTC * BTCWeight + returnETH * ETHWeight, 3)

weights = np.array([0.82, 0.18])
returns = prices.pct_change()
covariance = 365 * returns.cov()
variance = np.dot(weights.T, np.dot(covariance, weights))
print(str(np.round(variance, 3) * 100) + "%")

# We get 63.6% variance for our portfolio, which translates to an annual standard deviation of 79.73%. Even though we
# were in relatively risky stocks, the standard deviation of that portfolio (32.14%) pales in comparison to this.
# Even though it's riskier, the crypto portfolio also returned a much higher rate. This illustrates a classic
# financial principle: With more risk, there is more potential return. Can you think of one simple way we can compare
# the portfolios taking into account risk AND return?
#
# Yes, that's right, we can go back to the trusty Sharpe ratio.
#
# 4.2 Sharpe Ratio Comparison
# The Sharpe ratio of our stock portfolio was 1.821. If we run the same calculation on our crypto portfolio we get:
#
# 22647.01/5 = 4,529.40% as our annual percentage return. If we divide this by the standard deviation we get:
#
# 45.294/.7973 = 56.81 Sharpe Ratio
#
# This is a truly outstanding Sharpe ratio, and it's obvious at this point that if you had invested in Bitcoin or
# Ethereum five years ago and held it today, you're in very good shape. While this would've been a great investment,
# hindsight is 20/20, and it must be said that just because the last five years had incredible returns, it does not
# mean the next five years will.
