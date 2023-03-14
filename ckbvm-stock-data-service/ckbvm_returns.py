import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'


def calculate_returns(daily_data, include_date=False, include_price=False, make_csv=False, name=None):
    if name is not None:
        print("Calculating returns for " + name)
    else:
        print("Calculating returns")

    if len(daily_data) == 0:
        print("Dataframe given is empty.")
        return

    df = daily_data
    if len(df) > 1200:
        raise ValueError("Size reduced to 1200 rows")

    df["Date"] = df.index
    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df = df.rename({'Close Price': 'Close'}, axis='columns')

    actual_start_date = (df.iloc[0]["Date"]).strftime('%Y-%m-%d')
    actual_end_date = (df.iloc[-1]["Date"]).strftime('%Y-%m-%d')

    df = df.drop_duplicates()
    try:
        df = df.pivot(index="Date", columns="Close")
    except KeyError as e:
        print("Check data provided and index type", e)
        return

    start_date = df.index.min() - pd.DateOffset(day=1)
    end_date = df.index.max() + pd.DateOffset(day=31)
    dates = pd.date_range(start_date, end_date, freq='D')
    dates.name = 'Date'
    df = df.reindex(dates, method='ffill')
    df = df.stack('Close')
    df = df.sort_index(level=0)
    df = df.reset_index()

    df.index = df["Date"]
    df = (df[actual_start_date:actual_end_date])
    df = df.asfreq(freq="1D")
    df["Date"] = pd.to_datetime(df["Date"])

    shift_by = [1, 7, 30, 91]
    time_periods = ['1 Day', '1 Week', '1 Month', '3 Month']

    for i in range(len(shift_by)):

        if include_date is True:
            df[time_periods[i] + ' Date'] = (df.Date.shift(shift_by[i])).dt.date

        if include_price is True:
            df[time_periods[i] + ' Price'] = df["Close"].shift(shift_by[i])

        df[time_periods[i] + ' Returns'] = round((df["Close"] / df["Close"].shift(shift_by[i]))*100 - 100, 2)

    ar = (np.where(df["1 Day Returns"] == 0))
    df.drop(df.index[ar], inplace=True)

    df["Date"] = pd.to_datetime(df["Date"]).dt.date
    df.index = df["Date"]

    try:
        df.drop(columns=["Date", 'Open', 'High', 'Low', 'Shares Traded', 'Turnover (Rs. Cr)'], inplace=True)
    except KeyError:
        df.drop(
            columns=['Date', 'Symbol', 'Series', 'Open Price', 'High Price', 'Low Price', 'Last Price', 'Average Price',
                     'Total Traded Quantity', 'Turnover', 'No. of Trades', 'Deliverable Qty', '% Dly Qt to Traded Qty'],
            inplace=True)

    df = df.iloc[::-1]
    df.fillna('-', inplace=True)
    df = df.iloc[:1]

    if make_csv is True:

        if name is None:
            df.to_csv("data.csv", float_format='%.2f')
            print("File created : data.csv")
        else:
            df.to_csv("{}.csv".format(name), float_format='%.2f')
            print("File created : {}.csv".format(name))

    return df
