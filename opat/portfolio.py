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
    """
    Aggregate trade data to create day by date holdings information
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
            - Average Cost: weighted average cost of holdings
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

    # Create dataframe for output
    holdings = pd.DataFrame(
        columns=["Date", "Contract", "Type", "Average Cost", "Quantity"])
    holdings_last = pd.DataFrame(
        columns=["Date", "Contract", "Type", "Average Cost", "Quantity"])

    # Holdings will be created for every trade day between the start_date
    # and end_date
    trade_days = pd.date_range(start_date, end_date, freq='B')

    for date in trade_days:
        # Initiate every day's holdings as previous day's holdings
        holdings_now = holdings_last
        holdings_now["Date"] = date

        # When there are trades on the date, update the holdings to reflect
        # these changes.
        if date in trades.index:
            # Loop through each trade
            execution = trades[trades.index == date]
            for index, row in execution.iterrows():
                # Buy:  positive change in quantity
                # Sell: negative change in quantity
                if row["Action"] == "Buy":
                    delta_quantity = row["Quantity"]
                elif row["Action"] == "Sell":
                    delta_quantity = -row["Quantity"]
                else:
                    continue

                # If the contract already exist in the current holdings,
                # update the current holdings and recompute average cost
                if row["Contract"] in holdings_now["Contract"].values:
                    holdings_change = (
                        holdings_now["Contract"] == row["Contract"])
                    holdings_now.loc[holdings_change, "Quantity"] = (
                        holdings_now.loc[holdings_change, "Quantity"] + delta_quantity)
                    # Average cost = (current cost * current quantity + new cost * change in quantity)/total quantity
                    holdings_now.loc[holdings_change, "Average Cost"] = (
                        holdings_now.loc[holdings_change, "Average Cost"] * holdings_now.loc[holdings_change, "Quantity"] +
                        delta_quantity * row["Price"]) / (holdings_now.loc[holdings_change, "Quantity"] + delta_quantity)
                # If the contract is a new holding, initialize the holding
                else:
                    holdings_new = pd.DataFrame(
                        data={"Date": [date],
                              "Contract": [row["Contract"]],
                              "Type": [row["Type"]],
                              "Quantity": [delta_quantity],
                              "Average Cost": [row["Price"]]},
                        columns=["Date", "Contract", "Type", "Average Cost", "Quantity"])
                    holdings_now = holdings_now.append(
                        holdings_new, ignore_index=True)

        holdings_last = holdings_now
        holdings = holdings.append(holdings_last)

    holdings = holdings.reset_index(drop=True)

    return(holdings)
