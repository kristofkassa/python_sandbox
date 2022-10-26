# COMPARING AND CONTRASTING RETURNS OF DIFFERENT ASSET CLASSES

import datetime

import numpy as np
import pandas_datareader.data as web
import seaborn as sns
from matplotlib import pyplot as plt


start = datetime.date.today() - datetime.timedelta(days=5 * 365)
end = datetime.date.today()
df = web.DataReader(["TSLA", "NASDAQCOM", "CBBTCUSD"], "fred", start, end)

df = df.dropna()
df["SP500"] = np.log(df.sp500) - np.log(df.sp500.shift(1))
df["NASDAQ"] = np.log(df.NASDAQCOM) - np.log(df.NASDAQCOM.shift(1))
df["Bitcoin"] = np.log(df.CBBTCUSD) - np.log(df.CBBTCUSD.shift(1))
df = df.iloc[1:, 3:]

df.head()

df.describe()

df["2019-05-01":"2019-05-31"].plot()

df.std()

ax1 = df.plot(figsize=(15, 3), y="SP500", title="Figure 1: S&P 500 Daily Returns")
ax2 = df.plot(figsize=(15, 3), y="Bitcoin", title="Figure 2: Bitcoin Daily Returns")

ax1.set_ylim(-0.5, 0.4)
ax2.set_ylim(-0.5, 0.4)

# Covariance and Correlation

df.cov()

# Pearson correlation coefficient

corr = round(df.corr(), 3)
print(corr)

# # This relationship shows nearly perfect correlation.
# chart = sns.regplot(x="SP500", y="NASDAQ", data=df).set(
#     title="Figure 3: Daily S&P 500 Returns vs NASDAQ Returns"
# )
#
# plt.axvline(0, 0, 1, dash_capstyle="butt", linestyle="--", color="grey")
#
# plt.plot([min(df.SP500), max(df.SP500)], [0, 0], linestyle="--", color="grey")
#
# # The relationship here is much more scattered
# sns.regplot(x="SP500", y="Bitcoin", data=df).set(
#     title="Figure 4: Daily S&P 500 Returns vs Bitcoin Returns"
# )
#
# plt.axvline(0, 0, 1, dash_capstyle="butt", linestyle="--", color="grey")
#
# plt.plot([min(df.SP500), max(df.SP500)], [0, 0], linestyle="--", color="grey")
#
# plt.show()
#
# # 3.3 The Sharpe Ratio allows an investor to understand the relationship between the return of an
# # investment in relation to its volatility.
#
# Sharpe_Ratio_SP500 = df["SP500"].mean() / df["SP500"].std()
# print(Sharpe_Ratio_SP500)
#
# Sharpe_Ratio_Bitcoin = df["Bitcoin"].mean() / df["Bitcoin"].std()
# print(Sharpe_Ratio_Bitcoin)
#
# # Semivariance, a.k.a. downside risk, is a more refined version of a standard deviation. Standard deviation looks at
# # both the upside and downside risk of an investment.
#
# df[df["SP500"] < df["SP500"].mean()]["SP500"].std()
#
# df[df["Bitcoin"] < df["Bitcoin"].mean()]["Bitcoin"].std()
