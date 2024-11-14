### Detailed README.md

# S&P 500 Stock Analysis and Visualization

This project automates the process of retrieving and analyzing financial data for the top 50 companies in the S&P 500 index. It scrapes data from multiple financial websites, performs various calculations, and generates visualizations to provide insights into stock performance. The project also identifies companies with a "Buy" analyst rating, making it a valuable tool for investment decision-making.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Data Scraping Details](#data-scraping-details)
6. [Data Processing](#data-processing)
7. [Visualization](#visualization)
8. [Output Files](#output-files)
9. [Directory Structure](#directory-structure)
10. [Contributing](#contributing)
11. [License](#license)

## Project Overview

This project scrapes and analyzes financial data for the top 50 companies in the S&P 500 index. It retrieves data from Yahoo Finance and MarketBeat, calculates various metrics such as P/E ratios, and generates visualizations of stock prices. Additionally, it identifies companies with a "Buy" analyst rating and saves the data for further analysis.

## Features

- Scrapes ticker symbols and company names of the top 50 S&P 500 stocks from SlickCharts.
- Retrieves detailed financial data from Yahoo Finance, including:
  - Country
  - Industry
  - Stock Exchange
  - Forward P/E Difference
  - Daily closing prices for the year 2023
- Scrapes MarketBeat for:
  - Analyst rating
  - Upside/Downside potential
  - News sentiment
- Calculates the difference between forward and trailing P/E ratios.
- Generates plots for daily closing prices of stocks within the same industry.
- Identifies companies with a "Buy" analyst rating and saves this data separately.
- Outputs data to Excel files and saves plots as PNG images.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/sp500-stock-analysis.git
   ```
2. Navigate to the project directory:
   ```sh
   cd sp500-stock-analysis
   ```
3. Install the required Python packages:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script to scrape data, calculate metrics, and generate plots:

   ```sh
   python main.py
   ```
2. The script will perform the following tasks:

   - Scrape S&P 500 data from SlickCharts.
   - Retrieve financial data from Yahoo Finance.
   - Scrape MarketBeat for analyst ratings and news sentiment.
   - Calculate the difference between forward and trailing P/E ratios.
   - Generate plots for daily closing prices by industry.
   - Identify companies with a "Buy" analyst rating and save the data to an Excel file.

## Data Scraping Details

### SlickCharts

- URL: https://www.slickcharts.com/sp500
- Data Scraped: Ticker symbols and company names of the top 50 S&P 500 companies.

### Yahoo Finance

- Profile URL Example: https://ca.finance.yahoo.com/quote/{ticker}/profile
- Data Scraped:

  - Country
  - Industry
  - Stock Exchange
- Statistics URL Example: https://finance.yahoo.com/quote/{ticker}/key-statistics
- Data Scraped:

  - Forward P/E
  - Trailing P/E
  - P/E Difference (Forward P/E - Trailing P/E)
- Historical Data URL Example: https://ca.finance.yahoo.com/quote/{ticker}/history
- Data Scraped: Daily closing prices for the year 2023

### MarketBeat

- URL Example: https://www.marketbeat.com/stocks/{exchange}/{ticker}/
- Data Scraped:
  - Analyst Rating
  - Upside/Downside Potential
  - News Sentiment

## Data Processing

1. **Calculating P/E Difference**:
   - The difference between Forward P/E and Trailing P/E is calculated for each stock.
2. **Filtering for "Buy" Ratings**:
   - The project identifies companies with an analyst rating of "Buy" and saves this data separately.

## Visualization

1. **Plotting Daily Closing Prices**:
   - The script generates plots for daily closing prices for each industry.
   - Each plot includes annotations for the maximum and minimum prices.

## Output Files

The script generates the following output files:

1. **combined_data.xlsx**: Contains the scraped data and calculated metrics for all top 50 S&P 500 companies.
2. **buy_ratings.xlsx**: Lists companies with a "Buy" analyst rating, along with relevant metrics.
3. **plots/**: Directory containing PNG plots of daily closing prices for each industry.

## Directory Structure

```sh
sp500-stock-analysis/
├── plots/
│   ├── Consumer_Electronics_prices.png
│   ├── Internet_Content_&_Information_prices.png
│   ├── Internet_Retail_prices.png
│   ├── Semiconductors_prices.png
│   └── ... (more plots)
├── combined_data.xlsx
├── buy_ratings.xlsx
├── main.py
├── requirements.txt
└── README.md
```
## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Additional Files

1. **requirements.txt**

   ```txt
   requests
   beautifulsoup4
   pandas
   matplotlib

2. **main.py**
