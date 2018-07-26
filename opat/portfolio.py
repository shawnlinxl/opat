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

import fix_yahoo_finance as yf


def create_holdings(trades, start_date=None, end_date=None):
    """
    Aggregate trade data to create day by date holdings information

    Parameters
    ----------
    trades : pd.Dataframe of trade reccords
        trades should have the following columns:
            - Date: this is the index of the dataframe of trade dates
            - Contract: the name/ticker of the product being traded
            - Type: the type of the product e.g. US Equity/FX
            - Price: the execution price
            - Quantity: number of contracts bought/sold
            - Action: whether this is buy/sell

    start_date: Defaults to None.
        None will use the first trade date as the first holding date. Otherwise,
        only create holdings after the respective start_date.
    end_date: Defaults to None.
        None will use the current date as the final holding date.

    Returns
    -------
    holdings: pandas.Dataframe
        holdings data in the following format:
            - Date: index column
            - Contract: the name/ticker of the product being held
            - Type:  the type of the product e.g. US Equity/FX
            - Quantity: number of contracts held
    """
    # Set default start_date and end_date if not provided
    if start_date is None:
        start_date = trades.index.min().to_pydatetime()
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    if end_date is None:
        end_date = datetime.today().replace(minute=0, hour=0, second=0, microsecond=0)
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Merge the action and quantity column into 1
    # First combine each day's trading into 1 number by contract,
    # then use the cumulative sum to find out the holdings
    trades["Quantity"] = trades["Quantity"] * \
        (trades["Action"].map({"Buy": 1, "Sell": -1}))
    holdings = trades.groupby(["Date", "Type", "Contract"])["Quantity"].sum()
    holdings = holdings.groupby(["Type", "Contract"]).cumsum()
    holdings = holdings.reset_index()

    # Expand to daily holdings
    # First expand to wide form and fill each column, then reset index to the
    # desired date series and gathers back to stacked form
    holdings = holdings.pivot(index="Date", columns="Contract")
    holdings = holdings.fillna(method="ffill")
    dates = pd.date_range(start_date, end_date, freq='B')
    dates.name = "Date"
    holdings = holdings.reindex(dates, method="ffill")
    holdings = holdings.stack("Contract")
    holdings = holdings.reset_index()
    holdings = holdings.set_index("Date")

    # Keep only non-zero holdings dates, in case contracts are sold
    holdings = holdings[holdings["Quantity"] != 0]

    return holdings


def get_holdings_equity_price(holdings, source="yahoo", start_date=None, end_date=None):
    """Get the price data that corresponds to the holdings data

    Parameters
    ----------
    holdings : pandas.DataFrame
        holdings data, must have:
            - Date: index
            - Contract: name of the stock traded
            - Type: the type of the contract must be US Equity
    source : str, optional
        where to retrieve the price information from (the default is "yahoo",
        which currently uses fix-yahoo-finance and scrapes from yahoo)
    start_date : str, optional
        string of date in %Y-%m-%d. If given, truncate the holdings to start on
        or after the start_date (the default is None, which does not do any
        truncation)
    end_date : str, optional
        string of date in %Y-%m-%d. If given, truncate the holdings to end on
        or before the end_date (the default is None, which does not do any
        truncation)

    Returns
    -------
    price_data: pandas.DataFrame
        dataframe with:
            - Date: index
            - Open
            - High
            - Low
            - Close
            - Adj Close
            - Volume
            - Dividends
            - Stock Splits
            - Ticker
    """

    holdings = holdings[holdings["Type"] == "US Equity"]
    if start_date is not None:
        holdings = holdings[holdings.index >= start_date]
    if end_date is not None:
        holdings = holdings[holdings.index <= end_date]

    tickers = holdings["Contract"].unique()
    price_data = list()
    for ticker in tickers:
        holding_dates = holdings[holdings["Contract"] == ticker].index
        holding_min = holding_dates.min()
        holding_max = holding_dates.max()
        if source is "yahoo":
            prices = yf.download(
                [ticker], start=holding_min, end=holding_max, actions=True, progress=False)
        prices["Ticker"] = ticker
        price_data.append(prices)

    price_data = pd.concat(price_data)
    return price_data
