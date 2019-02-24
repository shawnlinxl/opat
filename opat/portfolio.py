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
from datetime import datetime


def create_holdings(trades, start_date=None, end_date=None):
    """ Aggregate trade data to create day by date holdings information

    Arguments:
        trades {DataFrame} -- trade records
            trades should have the following columns:
            - tradeday: this is the index of the dataframe of trade dates
            - ticker: the name/ticker of the product being traded
            - quantity: number of contracts bought/sold
            - action: whether this is buy/sell

    Keyword Arguments:
        start_date {string} -- None will use the first trade date as the first holding date. Otherwise,
        only create holdings after the respective start_date. (default: {None})
        end_date {string} -- None will use the current date as the final holding date. (default: {None})

    Returns:
        [DataFrame] -- holdings data in the following format:
            - tradeday
            - ticker
            - quantity: number of contracts held
    """

    # Set default start_date and end_date if not provided
    if start_date is None:
        start_date = trades["tradeday"].min().date()
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    if end_date is None:
        end_date = datetime.now().date()
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Merge the action and quantity column into 1
    # First combine each day's trading into 1 number by contract,
    # then use the cumulative sum to find out the holdings
    trades["quantity"] = trades["quantity"] * \
        (trades["action"].map({"Buy": 1, "Sell": -1}))
    holdings = trades.groupby(["tradeday", "ticker"])["quantity"].sum()
    holdings = holdings.groupby(["ticker"]).cumsum()
    holdings = holdings.reset_index()

    # Expand to daily holdings
    # First expand to wide form and fill each column, then reset index to the
    # desired date series and gathers back to stacked form
    holdings = holdings.pivot(index="tradeday", columns="ticker")
    holdings = holdings.fillna(method="ffill")
    dates = pd.date_range(start_date, end_date, freq='B')
    dates.name = "tradeday"
    holdings = holdings.reindex(dates, method="ffill")
    holdings = holdings.stack("ticker")
    holdings = holdings.reset_index()

    # Keep only non-zero holdings dates, in case contracts are sold
    holdings = holdings[holdings["quantity"] != 0]

    return holdings
