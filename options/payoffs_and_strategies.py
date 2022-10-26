import numpy as np
from scipy.stats import norm
from py_vollib.black_scholes import black_scholes as bs
from py_vollib.black_scholes.greeks.analytical import vega
from matplotlib import pyplot as plt
import opstrat as op

def black_scholes(r, S0, K, T, sigma, option_type='c'):
    """Compute the B-S price of a European Option
        S0: initial stock price
        K:  strike price
        T:  maturity
        r:  risk-free rate
        sigma: volatility
        option_type: type
    """
    print(f"B-S price parameters:\nS0={S0}\nK={K}\nT={T}\nsigma={sigma}\nr={r}\n")
    d1 = (np.log(S0 / K) + (r + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    print('d1:', d1)
    d2 = d1 - sigma * np.sqrt(T)
    print('d2:', d2)
    try:
        if option_type == "c":
            price = S0 * norm.cdf(d1, 0, 1) - K * np.exp(-r * T) * norm.cdf(d2, 0, 1)
        elif option_type == "p":
            price = K * np.exp(-r * T) * norm.cdf(-d2, 0, 1) - S0 * norm.cdf(-d1, 0, 1)
        return price
    except:
        print("Please confirm option type, either 'c' for Call or 'p' for Put!")


def implied_vol(S0, K, T, r, market_price, option_type='c', tol=0.00001):
    """Compute the implied volatility of a European Option
        S0: initial stock price
        K:  strike price
        T:  maturity
        r:  risk-free rate
        market_price: market observed price
        option_type: type
        tol: user choosen tolerance
    """
    print(f"Implied volatility parameters:\nS0={S0}\nK={K}\nT={T}\nmarket_price={market_price}\nr={r}\n")
    max_iter = 200  # max number of iterations
    vol_old = 0.30  # initial guess
    for k in range(max_iter):
        bs_price = bs(option_type, S0, K, T, r, vol_old)
        Cprime = vega(option_type, S0, K, T, r, vol_old) * 100
        C = bs_price - market_price
        vol_new = vol_old - C / Cprime
        bs_new = bs(option_type, S0, K, T, r, vol_new)
        if abs(vol_old - vol_new) < tol or abs(bs_new - market_price) < tol:
            break
        vol_old = vol_new
    implied_vol = vol_old
    return implied_vol


# 1 Calculate B-S price

S0 = 52  # initial stock price
K = 50  # exercise price
T = 0.5  # maturity
r = 0.05  # interest rate
sigma = 0.22  # implied volatility

calculated_price = black_scholes(r, S0, K, T, sigma, option_type='c')
print("B-S price is : ", calculated_price)

# 2 Calculate implied volatility

c = 5  # market price of call option
implied_vol_est = implied_vol(S0, K, T, r, c, option_type='c')
print("Implied Volatility is : ", round(implied_vol_est, 2) * 100, "%")


# plot implied volatility
sigmas = np.linspace(0, 1, 100)
prices = list(map(lambda v: black_scholes(r, S0, K, T, v, option_type='c'), sigmas))

fig, ax = plt.subplots(figsize=(10, 6))
fig.subplots_adjust(bottom=0.15, left=0.2)

ax.set_xlabel('Implied Volatility (%)')
ax.set_ylabel('Option Price ($)')

ax.plot(sigmas*100, prices)
plt.plot(implied_vol_est*100, c, color='red', marker='.', markersize=10)

# plot payoff
op.single_plotter(spot=52, strike=50, op_type="c", tr_type="s", op_pr=c)

plt.show()

