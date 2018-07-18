import os

from opat.stats import (cum_return,
                        vami,
                        period_return,
                        annualized_return,
                        annualized_std,)

from opat.plot import (ts_to_hc_series,
                       highstock_line,)

from opat.portfolio import (create_holdings,)

from opat.io import read_ts_csv


__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

returns_data = read_ts_csv(__location__ + '/test_data/fund_return.csv')
trade_data = read_ts_csv(__location__ + '/test_data/trade_log.csv')

print(returns_data.head())
print(cum_return(returns_data).head())
print(vami(returns_data).head())
print(period_return(returns_data, "month").head())
print(period_return(returns_data, "week").head())
print(period_return(returns_data, "year").head())
print(period_return(returns_data, "quarter").head())
print(annualized_return(returns_data))
print(annualized_std(returns_data))

hc_series = ts_to_hc_series(vami(returns_data))
html_string = highstock_line(hc_series, title="VAMI")

with open(__location__ + '/examples/vami.html', 'w') as html_file:
    html_file.write(html_string)

print(create_holdings(trade_data))
