from opat.stats import (cum_return,
                        vami,)

from opat.io import read_ts_csv

returns_data = read_ts_csv(r"opat\tests\test_data\fund_return.csv")

print(returns_data.head())
print(type(returns_data))
print(cum_return(returns_data))
print(vami(returns_data))
