from opat.stats import (cum_return,
                        vami,)

from opat.io import read_ts_csv

import os

__location__ = os.path.realpath(os.path.join(os.getcwd(),
                                os.path.dirname(__file__)))

returns_data = read_ts_csv(__location__ + '/test_data/fund_return.csv')

print(returns_data.head())
print(type(returns_data))
print(cum_return(returns_data))
print(vami(returns_data))
