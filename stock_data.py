import datetime as dt
import os
import pandas as pd
import yfinance as yf
import string

def get_stock_file():
    ticker_to_company_name = pd.read_csv('secwiki_tickers.csv')
    ticker_to_company_name['Name'] = ticker_to_company_name['Name'].str.translate(str.maketrans('','', string.punctuation))
    ticker_to_company_name['Name'] = ticker_to_company_name['Name'].str.upper()
    ticker_to_company_name['Name'] = ticker_to_company_name['Name'].str.strip()
    return ticker_to_company_name

def find_ticker_data(company_name):
    ticker_to_company_df = get_stock_file()
    if not is_valid_company(company_name):
        print("Not a valid company")
        return None
    try:
        company_name = company_name.translate(str.maketrans('','', string.punctuation))
        company_name = company_name.upper()
        company_name = company_name.strip()
        ticker = ticker_to_company_df.loc[ticker_to_company_df['Name'] == company_name]['Ticker'].iloc[0]
        company_sector = ticker_to_company_df.loc[ticker_to_company_df['Name'] == company_name]['Sector'].iloc[0]
        name = ticker_to_company_df.loc[ticker_to_company_df['Name'] == company_name]['Name'].iloc[0]
    except:
        print('This is not a valid company name.')
        print(company_name)
        return 'This is not a valid company name.'
    stock = yf.Ticker(ticker)
    stock_data=stock.history(period="1mo",actions=False,auto_adjust=False)
    stock_data['Symbol']=ticker
    stock_data['Sector']= company_sector
    stock_data['Company Name'] = name
    stock_data = stock_data[['Close', 'Symbol', 'Sector', 'Company Name']]
    stock_data.reset_index
    return stock_data

def up_down(df):
    day_change = []
    for i in range(len(df)):
        if i == 0:
            day_change.append(None)
            continue
        today = df.iloc[i,0]
        yesterday = df.iloc[i-1,0]
        if today >= yesterday:
            day_change.append('up')
        else:
            day_change.append('down')
    df['Price Change'] = day_change
    df.reset_index(inplace = True)
    df.sort_values(by = 'Date', inplace = True)
    return df.iloc[-7:]

def is_valid_company(company_name):
    ticker_df = get_stock_file()
    company_name = company_name.translate(str.maketrans('','', string.punctuation))
    company_name = company_name.upper()
    company_name = company_name.strip()
    if ticker_df.loc[ticker_df['Name'] == company_name].empty:
        return False
    else:
        return True

if __name__ == '__main__':
    pass