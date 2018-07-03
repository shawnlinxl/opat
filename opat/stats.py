#
# Copyright 2018 Shawn Lin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pandas as pd

def cum_return(returns):
    """
    Compute cumulative returns from simple returns.
    Parameters
    ----------
    returns : pd.Series of periodic returns

    Returns
    -------
    cumulative_returns : array-like
        Series of cumulative returns.
    """
    if len(returns) < 1:
        return returns.copy()

    # Allocate Memory
    result = returns.copy()

    # Compute cumulative return
    result = result.add(1, fill_value = 0)
    result = result.cumprod(skipna=True)
    result = result.add(-1)
    
    return result


def vami(returns, starting_value = 1000):
    """
    Compute VAMI (Value Added Monthly Index) from simple returns.
    Parameters
    ----------
    returns : pd.Series, np.ndarray, or pd.DataFrame
        Returns of the strategy as a percentage, noncumulative.
         - Time series with decimal returns.
         - Example::
            2015-07-16   -0.012143
            2015-07-17    0.045350
            2015-07-20    0.030957
            2015-07-21    0.004902
         - Also accepts two dimensional data. In this case, each column is
           cumulated.
    starting_value: float, optional
       The starting returns.
    
    Returns
    -------
    vami : array-like
        Series of cumulative returns.
    """
    result = cum_return(returns)
    result = result.add(1)
    result = result.multiply(starting_value)

    return result

def weekly_return(returns):
    """
    Compute weekly returns from higher frequency returns
    ----------
    returns : pd.Series of returns with periodicity shorter than a week

    Returns
    -------
    weekly_returns : array-like
        Series of weekly returns.
    """
    if len(returns) < 1:
        return returns.copy()

    # Allocate Memory
    result = returns.copy()

    # Compute cumulative return
    result = result.add(1, fill_value = 0)
    result = result.groupby(pd.Grouper(freq = "W")).prod()
    result = result - 1
    
    return result

def monthly_return(returns):
    """
    Compute monthly returns from higher frequency returns
    ----------
    returns : pd.Series of returns with periodicity shorter than a month

    Returns
    -------
    monthly_returns : array-like
        Series of monthly returns.
    """
    if len(returns) < 1:
        return returns.copy()

    # Allocate Memory
    result = returns.copy()

    # Compute cumulative return
    result = result.add(1, fill_value = 0)
    result = result.groupby(pd.Grouper(freq = "M")).prod()
    result = result - 1
    
    return result

def quarterly_return(returns):
    """
    Compute quarterly returns from higher frequency returns
    ----------
    returns : pd.Series of returns with periodicity shorter than a quarter

    Returns
    -------
    quarterly_returns : array-like
        Series of quarterly returns.
    """
    if len(returns) < 1:
        return returns.copy()

    # Allocate Memory
    result = returns.copy()

    # Compute cumulative return
    result = result.add(1, fill_value = 0)
    result = result.groupby(pd.Grouper(freq = "Q")).prod()
    result = result - 1
    
    return result

def annual_return(returns):
    """
    Compute annual returns from higher frequency returns
    ----------
    returns : pd.Series of returns with periodicity shorter than a year

    Returns
    -------
    annual_returns : array-like
        Series of annual returns.
    """
    if len(returns) < 1:
        return returns.copy()

    # Allocate Memory
    result = returns.copy()

    # Compute cumulative return
    result = result.add(1, fill_value = 0)
    result = result.groupby(pd.Grouper(freq = "Q")).prod()
    result = result - 1
    
    return result

def period_return(returns, period):
    """
    Convert higher frequency returns
    ----------
    returns : pd.Series of returns with higher frequency than the target
      periodicity

    Returns
    -------
    monthly_returns : array-like
        Series of annual returns.
    """
    return_func = {
        "week": weekly_return,
        "month": monthly_return,
        "quarter": quarterly_return,
        "year": annual_return,
    }

    result = returns.copy()
    result = return_func[period](returns)
    
    return result