import pandas as pd
import numpy as np
import datetime

def calculate_returns(prices):
    """
    Calculate daily returns from a price series.
    
    Args:
        prices (pd.Series): Series of prices
        
    Returns:
        pd.Series: Daily returns
    """
    return prices.pct_change().dropna()

def calculate_volatility(returns, window=21):
    """
    Calculate rolling volatility.
    
    Args:
        returns (pd.Series): Series of returns
        window (int): Window size for rolling volatility
        
    Returns:
        float: Volatility
    """
    return returns.std()

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    """
    Calculate Sharpe ratio.
    
    Args:
        returns (pd.Series): Series of returns
        risk_free_rate (float): Annual risk-free rate
        
    Returns:
        float: Sharpe ratio
    """
    # Convert annual risk-free rate to daily
    daily_risk_free_rate = (1 + risk_free_rate) ** (1/252) - 1
    
    # Calculate excess returns
    excess_returns = returns - daily_risk_free_rate
    
    # Calculate Sharpe ratio
    sharpe_ratio = excess_returns.mean() / excess_returns.std() * np.sqrt(252)
    
    return sharpe_ratio

def calculate_drawdown(prices):
    """
    Calculate maximum drawdown.
    
    Args:
        prices (pd.Series): Series of prices
        
    Returns:
        tuple: (max_drawdown, drawdown_series)
    """
    # Calculate rolling maximum
    rolling_max = prices.cummax()
    
    # Calculate drawdown
    drawdown = (prices / rolling_max - 1) * 100
    
    # Calculate maximum drawdown
    max_drawdown = drawdown.min()
    
    return max_drawdown, drawdown

def perform_monte_carlo(start_price, returns, days=30, simulations=1000):
    """
    Perform Monte Carlo simulation for price prediction.
    
    Args:
        start_price (float): Starting price
        returns (pd.Series): Series of historical returns
        days (int): Number of days to simulate
        simulations (int): Number of simulations
        
    Returns:
        pd.DataFrame: DataFrame with simulation results
    """
    # Parameters for simulation
    mu = returns.mean()
    sigma = returns.std()
    
    # Initialize results DataFrame
    simulation_results = pd.DataFrame()
    
    # Run simulations
    for i in range(simulations):
        # Generate random returns
        daily_returns = np.random.normal(mu, sigma, days)
        
        # Calculate price path
        price_path = [start_price]
        
        for r in daily_returns:
            price_path.append(price_path[-1] * (1 + r))
        
        # Add to results
        simulation_results[f'sim_{i}'] = price_path
    
    return simulation_results

def analyze_seasonality(prices, freq='month'):
    """
    Analyze seasonality in price data.
    
    Args:
        prices (pd.Series): Series of prices
        freq (str): Frequency to analyze ('month', 'day_of_week')
        
    Returns:
        pd.Series: Average returns by frequency
    """
    # Calculate returns
    returns = prices.pct_change().dropna()
    
    if freq == 'month':
        # Get month from index
        months = returns.index.month
        
        # Group by month and calculate mean return
        seasonal_returns = returns.groupby(months).mean() * 100
        
        # Map month numbers to names
        month_names = {
            1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
            7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
        }
        
        seasonal_returns.index = seasonal_returns.index.map(month_names)
        
    elif freq == 'day_of_week':
        # Get day of week from index
        days = returns.index.dayofweek
        
        # Group by day of week and calculate mean return
        seasonal_returns = returns.groupby(days).mean() * 100
        
        # Map day numbers to names
        day_names = {
            0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri'
        }
        
        seasonal_returns.index = seasonal_returns.index.map(day_names)
    
    return seasonal_returns

def calculate_beta(stock_returns, market_returns):
    """
    Calculate beta (sensitivity to market).
    
    Args:
        stock_returns (pd.Series): Stock returns
        market_returns (pd.Series): Market returns
        
    Returns:
        float: Beta value
    """
    # Align the two series
    aligned_data = pd.concat([stock_returns, market_returns], axis=1).dropna()
    stock_returns_aligned = aligned_data.iloc[:, 0]
    market_returns_aligned = aligned_data.iloc[:, 1]
    
    # Calculate covariance and variance
    covariance = stock_returns_aligned.cov(market_returns_aligned)
    market_variance = market_returns_aligned.var()
    
    # Calculate beta
    beta = covariance / market_variance
    
    return beta

def calculate_value_at_risk(returns, confidence_level=0.95):
    """
    Calculate Value at Risk (VaR).
    
    Args:
        returns (pd.Series): Series of returns
        confidence_level (float): Confidence level
        
    Returns:
        float: Value at Risk
    """
    # Calculate percentile
    var = returns.quantile(1 - confidence_level)
    
    return var * 100  # Return as percentage