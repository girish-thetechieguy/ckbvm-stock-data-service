import datetime

import pandas as pd

from ckbvm_scraper import scrape_data, scrape_bonus_splits, scrape_symbol

pd.options.mode.chained_assignment = None


def get_data(symbol, full_data=False, start_date=None, end_date=None, series="EQ"):
    print(start_date)
    print(end_date)
    
    symbol = symbol.replace('&', '%26')
    symbol_count = scrape_symbol(symbol)

    if full_data is True:
        parsed_start_date = datetime.datetime.strptime('1-1-1992', "%d-%m-%Y")
        parsed_end_date = datetime.datetime.today()

    else:

        if start_date is None or end_date is None:
            raise ValueError("Provide start and end date.")

        parsed_start_date = parse_date(start_date)
        parsed_end_date = parse_date(end_date)

        if parsed_start_date > parsed_end_date:
            raise ValueError("Starting date is greater than end date.")

    result = scrape_data(
        parsed_start_date, parsed_end_date, 'stock', stock_symbol=symbol, symbol_count=symbol_count, series=series)
    return result


def get_adjusted_data(symbol, df):
    
    headers = ['Open Price', 'High Price', 'Low Price',
           'Last Price', 'Close Price', 'Average Price']

    symbol = symbol.replace('&', '%26')

    if df.empty:
        print("Please check data. Dataframe is empty")
        return df

    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    try:
        df = df.drop(['Prev Close'], axis=1)
    except KeyError:
        pass

    ratio, dates = scrape_bonus_splits(symbol)
    for index in range(len(dates)):

        date = datetime.datetime.strptime(dates[index], '%d-%b-%Y')
        changed_data = df.loc[df.index < date]
        same_data = df.loc[df.index >= date]

        for header_index in headers:
            try:
                changed_data.loc[:, header_index] = changed_data.loc[:, header_index] / ratio[index]
            except TypeError:
                pass

        df = pd.concat([changed_data, same_data])

    return df


def get_adjusted_stock(symbol, full_data=False, start_date=None, end_date=None):
    df = get_data(symbol, full_data, start_date, end_date)
    df = get_adjusted_data(symbol, df)

    return df


def parse_date(text):
    for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass

    raise ValueError('Dates should be in YYYY-MM-DD or DD-MM-YYYY format')
