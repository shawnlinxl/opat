#
# Copyright 2019 Shawn Lin
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


def create_holdings(trades, splits=None):
    """ Aggregate trade data to create day by date holdings information

    Arguments:
        trades {DataFrame} -- trade records
            trades should have the following columns:
            - tradeday: this is the index of the dataframe of trade dates
            - ticker: the name/ticker of the product being traded
            - quantity: number of contracts bought/sold
            - action: whether this is buy/sell



    Keyword Arguments:
        splits {DataFrame} -- split records for each ticker (default: {None})
            splits should have the following columns:
            - tradeday
            - ticker
            - split: the split ratio

    Returns:
        [DataFrame] -- holdings data in the following format:
            - tradeday
            - ticker
            - quantity: number of contracts held
    """

    # Set start_date and end_date
    start_date = trades["tradeday"].min().date()
    end_date = datetime.now().date()

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

    if splits is not None:

        # Merge with splits and add split to holdings
        splits = splits[["tradeday", "ticker", "split"]]
        splits = holdings.merge(splits, how="left", on=["tradeday", "ticker"])
        splits["split"] = splits["split"].fillna(value=1)

        holdings = pd.DataFrame()

        for _, value in splits.groupby("ticker"):
            value = value.set_index("tradeday")
            value["prev_holding"] = value["quantity"].shift(1, fill_value=0)
            value["quantity"] = value["prev_holding"] * \
                (value["split"] - 1) + value["quantity"]
            value = value.reset_index()
            holdings = holdings.append(
                value[["tradeday", "ticker", "quantity"]], ignore_index=True)

    holdings = holdings.sort_values(by=["tradeday", "ticker"]).reset_index(drop=True)
    return holdings


def create_pnl(trades, prices):
    """Create daily portfolio dollar pnl from holdings and trades

    Arguments:
        trades {DataFrame} -- Daily trade data
        prices {DataFrame} -- Daily price data, with dividend and split information
    """

    # Create Holdings from trades
    holdings = create_holdings(trades, prices)

    # Merge holdings and trades with price data
    holdings = holdings.merge(prices, how="left", on=["tradeday", "ticker"])
    trades = trades.merge(prices, how="left", on=["tradeday", "ticker"])

    # Calculate pnl from holdings and new trades
    holdings_pnl = pd.DataFrame()
    trades_pnl = pd.DataFrame()

    for _, value in holdings.groupby("ticker"):
        value = value.set_index("tradeday")
        value["close"] = value["close"].fillna(method="ffill")
        value["prev_holding"] = value["quantity"].shift(1, fill_value=0)
        value["price_change"] = value["close"] - value["close"].shift(1)
        value["pnl"] = value["price_change"] * value["prev_holding"] + \
            value["dividend"] * value["prev_holding"]
        value = value.reset_index()
        holdings_pnl = holdings_pnl.append(
            value[["tradeday", "ticker", "pnl"]], ignore_index=True)

    for _, value in trades.groupby("ticker"):
        value = value.set_index("tradeday")
        value["close"] = value["close"].fillna(method="ffill")
        value["price_change"] = value["close"] - value["price"]
        value["pnl"] = value["price_change"] * value["quantity"] * \
            value["action"].map({"Buy": 1, "Sell": -1})
        value = value.reset_index()
        trades_pnl = trades_pnl.append(
            value[["tradeday", "ticker", "pnl"]], ignore_index=True)

    # Combine pnl into pnl by ticker
    pnl = holdings_pnl.append(trades_pnl, ignore_index=True)
    pnl = pnl.groupby(["tradeday", "ticker"]).sum()

    return pnl
