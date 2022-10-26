# Types of Financial Data

import investpy

# Let's use the investpy package to get Argentinian bond data.

data = investpy.get_bond_historical_data(
    bond="Hungary 3Y", from_date="01/01/2018", to_date="31/12/2021"
)
print(data)
