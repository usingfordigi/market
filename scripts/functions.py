import plotly.graph_objects as go


def stock_chart(stock_object, period):
    """
    Returns an interactive plot of stock price against time period specified.

    Parameters
    ----------

    stock_object: yfinance.ticker.Ticker
        Stock Ticker Object

    period: str
        Time period in str format.
        It can take values ['1d', '1mo', '3mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

    Returns
    -------

    fig: plotly.graph_objs._figure.Figure
        Plotly figure object

    """

    period_list = ['1d', '1mo', '3mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    if period not in period_list:
        raise KeyError("Incorrect period specified. Allowed list: "
                       "['1d','1mo','3mo','1y','2y','5y','10y','ytd','max']")

    # Intervals set similar to RH policy
    if period == '1d':
        interval = '5m'
    else:
        interval = '1d'

    data = stock_object.history(period=period, interval=interval)
    plot_title = 'Stock: {}, Time Period: {}'.format(stock_object.ticker, period)

    fig = go.Figure(
        data=go.Scatter(y=data['Close'],
                        x=data.index,
                        line=dict(color='chartreuse', width=4)
                        ),

    )

    fig.add_layout_image(
        dict(
            source=stock_object.info['logo_url'],
            xref="paper", yref="paper",
            x=1, y=1.05,
            sizex=0.2, sizey=0.2,
            xanchor="left", yanchor="bottom"
        )
    )

    fig.update_layout(title=plot_title,
                      hovermode="x",
                      yaxis_title='Closing Price',
                      template='plotly_dark',
                      xaxis_showgrid=False,
                      yaxis_showgrid=False
                      )

    return fig


def options_table(stock_object, date=None, kind='calls'):
    """
    Returns the info about options of a stock on any given date in tabular format.
    If `date` is not given, it fetches data for the next closest date. If `kind` is
    not specified, it returns data for calls.

    Parameters
    ----------

    stock_object: yfinance.ticker.Ticker
        Stock Ticker Object

    date: str, default None
        Date in str format. Should be amony `stock_object.options` list

    kind: str, default `calls`
        Type of options data to return. Takes either `calls` or `puts`

    Returns
    -------

    fig: plotly.graph_objs._figure.Figure
        Plotly table figure object

    """
    possible_dates = stock_object.options

    if date is None:
        date = possible_dates[0]
    if date not in possible_dates:
        raise KeyError('Invalid date selected. For available dates, try ticker_object.options')

    if kind == 'calls':
        data = stock_object.option_chain(date=date).calls

    elif kind == 'puts':
        data = stock_object.option_chain(date=date).puts

    else:
        raise KeyError('Invalid kind selected. Only `calls` and `puts` supported.')

    data = data[['strike',
                 'lastPrice',
                 'bid',
                 'ask',
                 'change',
                 'percentChange',
                 'volume',
                 'openInterest',
                 'impliedVolatility',
                 'inTheMoney']]

    data.columns = ['Strike', 'Last Price', 'Bid', 'Ask', 'Change', 'Percent Change',
                    'Volume', 'Open Interest', 'Implied Volatility', 'In The Money']

    data = data.round(3)
    bold_columns = ['<b>' + x + '</b>' for x in data.columns]

    fig = go.Figure(data=[go.Table(
        columnwidth=[1, 1.1, 1, 1, 1, 1.4, 1.1, 1.4, 1.5, 1.2],
        header=dict(values=bold_columns,
                    fill_color='black',
                    line_color='darkslategray',
                    font=dict(color='white', size=12),
                    align='center'),
        cells=dict(values=data.T.values.tolist(),
                   fill_color='white',
                   align='center'))
    ])

    return fig