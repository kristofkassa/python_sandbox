import datetime

import numpy as np
import pandas as pd
import pandas_datareader.data as web
import seaborn as sns
from matplotlib import pyplot as plt
from scipy import stats

start = datetime.date.today() - datetime.timedelta(365 * 20)
end = datetime.date.today()
prices = web.DataReader(["^GSPC"], "yahoo", start, end)["Adj Close"]

# Rename column to make names more intuitive
prices = prices.rename(columns={"^GSPC": "SP500"})
df = np.log(prices) - np.log(prices.shift(1))
df = df.iloc[1:, 0:]

print(df)

# Are returns symmetric?
(len(df[df.SP500 > df.SP500.mean()])) / (len(df))

vols = pd.DataFrame(df.SP500.rolling(50).std()).rename(columns={"SP500": "S&P 500 STD"})
# set figure size
plt.figure(figsize=(12, 5))
# plot using rolling average
sns.lineplot(
    x="Date",
    y="S&P 500 STD",
    data=vols,
    label="S&P 500 50 day standard deviation rolling avg",
)

# Are Stock Returns Normally Distributed?
df.hist(bins=100)

# Conducting a normality test
stats.normaltest((np.array(df.SP500)))

# Testing skewness and kurtosis
var = stats.jarque_bera((np.array(df.SP500))).pvalue

dfMax = df.SP500.max()
dfMin = df.SP500.min()
print(
    "Min return of sample data is %.4f and the maximum return of sample data is %.4f"
    % (dfMin, dfMax)
)

# Non-Gaussian Distributions
stats.t.rvs(df=5030, size=5000)

# generate t distribution with sample size 10000
x = stats.t.rvs(df=5030, size=10000)

# create plot of t distribution
plt.hist(x, density=True, edgecolor="black", bins=50)

plt.show()

t_stat, p = stats.ttest_ind(df["SP500"], stats.t.rvs(df=5030, size=5031))
print(f"t={t_stat}, p={p}")