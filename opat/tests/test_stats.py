import os
import pandas as pd

from opat.stats import (cum_return,
                        vami,
                        period_return,
                        annualized_return,
                        annualized_std,)

from opat.portfolio import (create_holdings)


def read_ts_csv(filepath):
    """
    Load timeseries from csv, the first column must be date indices
    ----------
    filepath: path to the time series csv file

    Returns
    -------
    time indexed Pandas Dataframe
    """
    result = pd.read_csv(filepath,
                         parse_dates=[0],
                         header=0,
                         index_col=0)

    return(result)


__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

returns_data = read_ts_csv(__location__ + '/test_data/fund_return.csv')
trade_data = read_ts_csv(__location__ + '/test_data/trade_log.csv')
price_data = read_ts_csv(__location__ + '/test_data/price_data.csv')

print(returns_data.head())
print(cum_return(returns_data).head())
print(vami(returns_data).head())
print(period_return(returns_data, "month").head())
print(period_return(returns_data, "week").head())
print(period_return(returns_data, "year").head())
print(period_return(returns_data, "quarter").head())
print(annualized_return(returns_data))
print(annualized_std(returns_data))
print(create_holdings(trade_data).head())
