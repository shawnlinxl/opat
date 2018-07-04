from opat.stats import (cum_return,
                        vami,
                        period_return,
                        annualized_return)

from opat.io import read_ts_csv

import os

__location__ = os.path.realpath(os.path.join(os.getcwd(),
                                os.path.dirname(__file__)))

returns_data = read_ts_csv(__location__ + '/test_data/fund_return.csv')

print(returns_data.head())
print(cum_return(returns_data).head())
print(vami(returns_data).head())
print(period_return(returns_data, "month").head())
print(period_return(returns_data, "week").head())
print(period_return(returns_data, "year").head())
print(period_return(returns_data, "quarter").head())
print(annualized_return(returns_data))
