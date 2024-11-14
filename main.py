import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os

# Ensure the necessary directory for saving plots exists
SAVE_DIR = 'plots'
os.makedirs(SAVE_DIR, exist_ok=True)
def clean_key(key):
    return key.replace('\u200b', '')
def scrape_sp500():
    """
    Scrapes the ticker symbols and company names of the top 50 stocks in the S&P 500.
    """
    print("Starting to scrape S&P 500 data...")
    url = 'https://www.slickcharts.com/sp500'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print("Successfully retrieved webpage for S&P 500 data.")
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'table table-hover table-borderless table-sm'})

        if table:
            print("Found S&P 500 table.")
            rows = table.find_all('tr')[1:51]  # Top 50 stocks
            tickers = []
            company_names = []

            for row in rows:
                cols = row.find_all('td')
                ticker = cols[2].text.strip()
                company_name = cols[1].text.strip()
                tickers.append(ticker)
                company_names.append(company_name)

            df_stocks = pd.DataFrame({'Ticker': tickers, 'Company Name': company_names})
            print("Finished scraping S&P 500 data.")
            return df_stocks
        else:
            print("Error: Table not found in the HTML content.")
    else:
        print(f"Error: Failed to retrieve the webpage for S&P 500 data. Status code: {response.status_code}")

def scrape_yahoo_finance(ticker):
    """
    Scrapes Yahoo Finance for the given ticker symbol to obtain country, industry, stock exchange,
    Forward P/E Difference, and daily closing prices for all of 2023.
    """
    print(f"Starting to scrape Yahoo Finance data for ticker {ticker}...")
    profile_url = f'https://ca.finance.yahoo.com/quote/{ticker}/profile'
    statistics_url = f'https://finance.yahoo.com/quote/{ticker}/key-statistics'
    history_url = f'https://ca.finance.yahoo.com/quote/{ticker}/history?period1=1672531200&period2=1703980800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Scrape profile data
    profile_response = requests.get(profile_url, headers=headers)
    if profile_response.status_code == 200:
        print("Successfully retrieved profile data.")
        profile_soup = BeautifulSoup(profile_response.text, 'html.parser')
        country = profile_soup.find('span', string='Country').find_next_sibling('span').text.strip() if profile_soup.find('span', string='Country') else 'N/A'
        industry = profile_soup.find('span', string='Industry').find_next_sibling('span').text.strip() if profile_soup.find('span', string='Industry') else 'N/A'
        exchange = 'NASDAQ' if 'NASDAQ' in profile_soup.text else 'NYSE'
    else:
        print(f"Error: Failed to retrieve profile data for {ticker}. Status code: {profile_response.status_code}")
        country, industry, exchange = 'N/A', 'N/A', 'N/A'

    # Scrape statistics data
    statistics_response = requests.get(statistics_url, headers=headers)
    if statistics_response.status_code == 200:
        print("Successfully retrieved statistics data.")
        statistics_soup = BeautifulSoup(statistics_response.text, 'html.parser')

        try:
            trailing_pe_value = statistics_soup.find('td', string='Trailing P/E').find_next_sibling('td').text.strip()
            trailing_pe = float(trailing_pe_value.replace(',', '')) if trailing_pe_value != '--' else None
        except (AttributeError, ValueError):
            trailing_pe = None

        try:
            forward_pe_value = statistics_soup.find('td', string='Forward P/E').find_next_sibling('td').text.strip()
            forward_pe = float(forward_pe_value.replace(',', '')) if forward_pe_value != '--' else None
        except (AttributeError, ValueError):
            forward_pe = None

        # Note: The following line assumes you have historical forward P/E data for 12/31/2023
        pe_difference = forward_pe - trailing_pe if forward_pe is not None and trailing_pe is not None else None
    else:
        print(f"Error: Failed to retrieve statistics data for {ticker}. Status code: {statistics_response.status_code}")
        trailing_pe, forward_pe, pe_difference = None, None, None

    # Scrape historical data
    history_response = requests.get(history_url, headers=headers)
    if history_response.status_code == 200:
        print("Successfully retrieved historical data.")
        history_soup = BeautifulSoup(history_response.text, 'html.parser')
        rows = history_soup.find_all('tr', {'class': 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})
        dates = []
        closing_prices = []

        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 4:
                date = cols[0].text.strip()
                close = cols[4].text.strip().replace(',', '')
                dates.append(date)
                closing_prices.append(float(close))

        df_prices = pd.DataFrame({'Date': dates, 'Close': closing_prices})
    else:
        print(f"Error: Failed to retrieve historical data for {ticker}. Status code: {history_response.status_code}")
        df_prices = pd.DataFrame()

    print(f"Finished scraping Yahoo Finance data for ticker {ticker}.")
    return {
        'Country': country,
        'Industry': industry,
        'Forward P/E': forward_pe,
        'P/E Difference': pe_difference,
        'Exchange': exchange,
        'Prices': df_prices
    }

def scrape_marketbeat_data(ticker, exchange):
    """
    Scrapes MarketBeat data for the given ticker symbol to obtain analyst rating, upside/downside,
    and news sentiment.
    """
    print(f"Starting to scrape MarketBeat data for ticker {ticker}...")
    url = f'https://www.marketbeat.com/stocks/{exchange}/{ticker}/'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = {}

    elements = soup.find_all('div', class_='col-md-3 col-sm-4 col-6 mb-2 marketrankRowOne')
    for element in elements:
        try:
            title = element.find('dt', class_='font-small text-uppercase font-weight-normal mb-2').text.strip()
            main_data = element.find('div', class_='key-stat').text.strip()
            additional_details = element.find('div', class_='key-stat-details').text.strip()
            if title and main_data:
                key = clean_key(title.strip())
                # marketbeat_data[key] = {'main_data': maindata.strip(), 'additional_data': additional_data.strip()}
                data[key] = {'main_data': main_data, 'additional_details': additional_details}
            print(f"title: {title}, main_data: {main_data}, additional_details: {additional_details}")
        except AttributeError as e:
            print(f"Error processing element for ticker {ticker}: {e}")

    # Check if 'Upside/Downside' is missing
    if 'Upside/Downside' not in data:
        print(f"Warning: 'Upside/Downside' data is missing for ticker {ticker}")

    print(f"Finished scraping MarketBeat data for ticker {ticker}.")
    return data


def plot_prices(df, industry):
    """
    Plots the daily closing prices for each stock in the given industry and annotates the maximum
    and minimum prices.
    """
    if industry == 'N/A':
        print(f"Skipping plot for industry: {industry}")
        return
    
    industry_df = df[df['Industry'] == industry]
    
    if industry_df.empty:
        print(f"No data to plot for industry: {industry}")
        return

    print(f"Plotting prices for industry: {industry}")
    plt.figure(figsize=(14, 8))
    
    for _, row in industry_df.iterrows():
        ticker = row['Ticker']
        prices_df = row['Prices']
        
        if not prices_df.empty:
            plt.plot(pd.to_datetime(prices_df['Date']), prices_df['Close'], label=ticker)
            max_price = prices_df['Close'].max()
            min_price = prices_df['Close'].min()
            max_date = prices_df[prices_df['Close'] == max_price]['Date'].values[0]
            min_date = prices_df[prices_df['Close'] == min_price]['Date'].values[0]
            plt.annotate(f'{max_price}', xy=(pd.to_datetime(max_date), max_price), xytext=(pd.to_datetime(max_date), max_price + 1), arrowprops=dict(facecolor='green', shrink=0.05))
            plt.annotate(f'{min_price}', xy=(pd.to_datetime(min_date), min_price), xytext=(pd.to_datetime(min_date), min_price - 1), arrowprops=dict(facecolor='red', shrink=0.05))

    plt.title(f'Daily Closing Prices for {industry} Stocks (2023)')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.legend(loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    
    plot_filename = f"{SAVE_DIR}/{industry.replace(' ', '_')}_prices.png"
    plt.savefig(plot_filename)
    print(f"Saved plot for industry '{industry}' as '{plot_filename}'")
    plt.close()

def save_to_excel(df, filename):
    """
    Saves the DataFrame to an Excel file.
    """
    print(f"Saving data to Excel file '{filename}'...")
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, index=False)
    print(f"Data saved to '{filename}'")

# Main script logic
# Main script logic
if __name__ == "__main__":
    df_sp500 = scrape_sp500()
    
    if df_sp500 is not None and not df_sp500.empty:
        records = []
        
        for index, row in df_sp500.iterrows():
            ticker = row['Ticker']
            company_name = row['Company Name']
            yahoo_data = scrape_yahoo_finance(ticker)
            marketbeat_data = scrape_marketbeat_data(ticker, yahoo_data['Exchange'])
            print(marketbeat_data.get('Upside/Downside', {}))
            record = {
                'Ticker': ticker,
                'Company Name': company_name,
                # 'Country': yahoo_data['Country'],
                'Industry': yahoo_data['Industry'],
                'Forward P/E': yahoo_data['Forward P/E'],
                'P/E Difference': yahoo_data['P/E Difference'],
                'Exchange': yahoo_data['Exchange'],
                'Prices': yahoo_data['Prices'],
                'Analyst Rating': marketbeat_data.get('Analyst Rating', {}).get('main_data', 'N/A'),
                'Upside/Downside': marketbeat_data.get('Upside/Downside', {}).get('main_data', 'N/A'),
                'News Sentiment': marketbeat_data.get('News Sentiment', {}).get('main_data', 'N/A')
            }
            
            # Debug print statements to verify data
            if record['Upside/Downside'] == 'N/A':
                print(f"Warning: 'Upside/Downside' is 'N/A' for ticker {ticker}")
            
            records.append(record)
        
        df_combined = pd.DataFrame(records)
        save_to_excel(df_combined, 'combined_data.xlsx')

        #  After scraping MarketBeat data, filter for "Buy" ratings
        buy_ratings = []
        for record in records:
            if 'Buy' in record['Analyst Rating']:
                buy_ratings.append({
                    'Company Name': record['Company Name'],
                    'Analyst Rating': record['Analyst Rating'],
                    'Upside/Downside': record['Upside/Downside'],
                    'News Sentiment': record['News Sentiment'],
                    'P/E Difference': record['P/E Difference']
                })
        df_buy_ratings = pd.DataFrame(buy_ratings)
        save_to_excel(df_buy_ratings, 'buy_ratings.xlsx')
        
        industries = df_combined['Industry'].unique()
        
        for industry in industries:
            plot_prices(df_combined, industry)
        
        print("All tasks completed successfully.")
    else:
        print("Failed to retrieve or process S&P 500 data.")
