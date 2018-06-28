from opat.stats import (cum_return,
                        vami,)
import pandas as pd

returns_data = pd.read_csv(r"opat\tests\test_data\fund_return.csv", parse_dates=[0])
returns_data = returns_data.set_index("date")

print(returns_data.head())
print(type(returns_data))
print(cum_return(returns_data))
print(vami(returns_data))
