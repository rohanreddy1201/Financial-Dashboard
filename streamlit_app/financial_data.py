import requests
import pandas as pd
from datetime import datetime

API_KEY = 'FJQDEKYB3PWCQODT'

def get_stock_symbols():
    # Static list of popular stock symbols
    symbols = ['AAPL', 'GOOGL', 'AMZN', 'MSFT', 'TSLA', 'FB', 'NVDA', 'NFLX', 'BABA', 'V']
    return symbols

def get_stock_data(symbol, date_range):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}&outputsize=full'
    response = requests.get(url)
    data = response.json()
    
    if 'Time Series (Daily)' not in data:
        raise ValueError(f"Unexpected response format: {data}")

    time_series = data['Time Series (Daily)']
    records = []
    for date, daily_data in time_series.items():
        records.append({
            'Date': date,
            'Open': float(daily_data['1. open']),
            'High': float(daily_data['2. high']),
            'Low': float(daily_data['3. low']),
            'Close': float(daily_data['4. close']),
            'Volume': int(daily_data['5. volume'])
        })

    df = pd.DataFrame(records)
    df['Date'] = pd.to_datetime(df['Date'])

    # Convert date_range to datetime
    start_date = datetime.combine(date_range[0], datetime.min.time())
    end_date = datetime.combine(date_range[1], datetime.min.time())

    df = df[df['Date'].between(start_date, end_date)]
    df.sort_values('Date', inplace=True)
    return df