#
# Copyright 201 Shawn Lin
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
import numpy as np

def cum_returns(returns):
    """
    Compute cumulative returns from simple returns.
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

    Returns
    -------
    cumulative_returns : array-like
        Series of cumulative returns.
    """
    if len(returns) < 1:
        return returns.copy()

    # Fill NA with 0
    nan_mask = np.isnan(returns)
    if np.any(nan_mask):
        returns = returns.copy()
        returns[nan_mask] = 0

    # Allocate Memory
    result = np.empty_like(returns)

    # Compute cumulative return
    np.add(returns, 1, out=result)
    result.cumprod(axis=0)
    np.subtract(result, 1, out=result)

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

    result = cum_returns(returns)
    np.add(result, 1, out=result)
    np.multiply(result, starting_value, out=result)