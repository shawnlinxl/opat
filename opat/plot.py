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

import numpy as np


def ts_to_hc_series(df):
    """
    Convert time series data to highchart series format
    ----------
    df : pd.Series, pd.DataFrame
        A pandas dataframe with datetime as index

    Returns
    -------
    highchart_series : json
        JSON format string of time which has column and time in the format
        [{'name' : col1,
          'data' : [[date1, value1], [date2, value2]]}]
    """

    # Put dataframe into highchart format
    result = [{'name': key, 'data': list([list(a) for a in zip(value.index.astype(np.int64) // 10 ** 6, value.values)])}
              for key, value in df.items()]

    return(result)


def highstock_line(hc_data, title=None, width="800px", height="600px"):
    """
    Convert time series data to highchart series format
    ----------
    hc_data : JSON
        A highchart JSON with datetime as index and cumulative_returns as
        value.
    title: string
        title of the plot
    width: string
        plot width in pixels
    height: string
        plot height in pixels

    Returns
    -------
    highstock object: HTML
    """

    if title is None:
        title = ""

    template = """
        <html>
        <head>
            <script src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
            <script src="https://code.highcharts.com/stock/highstock.js"></script>
            <script src="https://code.highcharts.com/stock/modules/exporting.js"></script>
            <script src="https://code.highcharts.com/stock/modules/export-data.js"></script>

        </head>
        <body>

        <div id="container" style="width: {width}; height: {height}; margin: 125 auto"></div>

        <script language="JavaScript">
            Highcharts.stockChart('container', {{

                series : {data},

                rangeSelector: {{
                    selected: 4
                }},

                tooltip: {{
                    pointFormat: '<span style="color:{{series.color}}">{{series.name}}</span>: <b>{{point.y}}</b> ({{point.change}}%)<br/>',
                    valueDecimals: 2,
                    split: true
                }},

                yAxis: {{
                    labels: {{
                        formatter: function () {{
                            return (this.value > 0 ? ' + ' : '') + this.value + '%';
                        }}
                    }},
                    plotLines: [{{
                        value: 0,
                        width: 2,
                        color: 'silver'
                    }}]
                }},

                plotOptions: {{
                    series: {{
                        compare: 'percent'
                    }}
                }},

                legend: {{
                    enabled: true
                }},

                title: {{
                    text: '{title}'
                }},

            }});
        </script>

        </body>
        </html>

    """

    template = template.format(width=width,
                               height=height,
                               title=title,
                               data=hc_data)

    return(template)
