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
