import yfinance as yf
import pandas as pd
import requests
import datetime

def get_stock_data(ticker, start_date, end_date, interval="1d"):
    """
    Fetch stock market data for a given ticker and date range.
    
    Args:
        ticker (str): Stock ticker symbol
        start_date (datetime): Start date for data
        end_date (datetime): End date for data
        interval (str): Data interval (1d, 1h, 15m, etc.)
        
    Returns:
        pd.DataFrame: DataFrame with stock data
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date, interval=interval)
        
        if data.empty:
            raise ValueError(f"No data found for ticker {ticker} in the specified date range")
        
        return data
    except Exception as e:
        raise Exception(f"Error fetching stock data: {str(e)}")

def get_company_info(ticker):
    """
    Get company information for a given ticker.
    
    Args:
        ticker (str): Stock ticker symbol
        
    Returns:
        dict: Company information
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        company_info = {
            'name': info.get('shortName', info.get('longName', ticker)),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'description': info.get('longBusinessSummary', 'No description available'),
            'website': info.get('website', 'N/A'),
            'logo_url': info.get('logo_url', ''),
            'market_cap': info.get('marketCap', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'dividend_yield': info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
            'beta': info.get('beta', 0),
            'eps': info.get('trailingEps', 0),
            '52_week_high': info.get('fiftyTwoWeekHigh', 0),
            '52_week_low': info.get('fiftyTwoWeekLow', 0)
        }
        
        return company_info
    except Exception as e:
        # Return basic info if full info not available
        return {
            'name': ticker,
            'sector': 'N/A',
            'industry': 'N/A',
            'description': 'Information not available',
            'website': 'N/A',
            'logo_url': ''
        }

def get_news(ticker, limit=10):
    """
    Get news articles for a given ticker.
    
    Args:
        ticker (str): Stock ticker symbol
        limit (int): Maximum number of news articles
        
    Returns:
        list: List of news articles
    """
    try:
        stock = yf.Ticker(ticker)
        news_data = stock.news
        
        if not news_data:
            return []
        
        articles = []
        for article in news_data[:limit]:
            published_date = datetime.datetime.fromtimestamp(article.get('providerPublishTime', 0)).strftime('%Y-%m-%d')
            articles.append({
                'title': article.get('title', 'No title'),
                'published_date': published_date,
                'source': article.get('publisher', 'Unknown'),
                'url': article.get('link', '#'),
                'summary': article.get('summary', 'No summary available')
            })
        
        return articles
    except Exception as e:
        return []

def get_market_indices():
    """
    Get current market indices data.
    
    Returns:
        dict: Major market indices data
    """
    indices = {
        '^GSPC': 'S&P 500',
        '^DJI': 'Dow Jones',
        '^IXIC': 'NASDAQ',
        '^RUT': 'Russell 2000',
        '^FTSE': 'FTSE 100'
    }
    
    data = {}
    
    for ticker, name in indices.items():
        try:
            index = yf.Ticker(ticker)
            latest = index.history(period='1d')
            if not latest.empty:
                last_close = latest['Close'].iloc[-1]
                prev_close = index.history(period='2d')['Close'].iloc[-2]
                change = (last_close - prev_close) / prev_close * 100
                
                data[name] = {
                    'price': last_close,
                    'change_pct': change
                }
        except:
            pass
    
    return data