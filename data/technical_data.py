import pandas as pd
import numpy as np

def calculate_rsi(prices, window=14):
    """
    Calculate Relative Strength Index (RSI).
    
    Args:
        prices (pd.Series): Series of prices
        window (int): Period for RSI calculation
        
    Returns:
        pd.Series: RSI values
    """
    # Calculate price changes
    delta = prices.diff()
    
    # Separate gains and losses
    gain = delta.copy()
    loss = delta.copy()
    gain[gain < 0] = 0
    loss[loss > 0] = 0
    loss = abs(loss)
    
    # Calculate average gain and loss
    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()
    
    # Calculate RS
    rs = avg_gain / avg_loss
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_macd(prices, fast_period=12, slow_period=26, signal_period=9):
    """
    Calculate Moving Average Convergence Divergence (MACD).
    
    Args:
        prices (pd.Series): Series of prices
        fast_period (int): Fast EMA period
        slow_period (int): Slow EMA period
        signal_period (int): Signal line period
        
    Returns:
        pd.DataFrame: DataFrame with MACD, Signal and Histogram
    """
    # Calculate EMAs
    ema_fast = prices.ewm(span=fast_period, adjust=False).mean()
    ema_slow = prices.ewm(span=slow_period, adjust=False).mean()
    
    # Calculate MACD line
    macd_line = ema_fast - ema_slow
    
    # Calculate signal line
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    
    # Calculate histogram
    histogram = macd_line - signal_line
    
    # Create DataFrame with results
    macd_data = pd.DataFrame({
        'MACD': macd_line,
        'MACD_Signal': signal_line,
        'MACD_Hist': histogram
    })
    
    return macd_data

def calculate_bollinger_bands(prices, window=20, num_std=2):
    """
    Calculate Bollinger Bands.
    
    Args:
        prices (pd.Series): Series of prices
        window (int): Moving average window
        num_std (float): Number of standard deviations
        
    Returns:
        pd.DataFrame: DataFrame with Upper, Middle, and Lower bands
    """
    # Calculate middle band (SMA)
    middle_band = prices.rolling(window=window).mean()
    
    # Calculate standard deviation
    std = prices.rolling(window=window).std()
    
    # Calculate upper and lower bands
    upper_band = middle_band + (std * num_std)
    lower_band = middle_band - (std * num_std)
    
    # Create DataFrame with results
    bollinger_bands = pd.DataFrame({
        'BB_Upper': upper_band,
        'BB_Middle': middle_band,
        'BB_Lower': lower_band
    })
    
    return bollinger_bands

def calculate_moving_averages(prices, periods=[10, 20, 50, 200]):
    """
    Calculate Moving Averages for multiple periods.
    
    Args:
        prices (pd.Series): Series of prices
        periods (list): List of periods for moving averages
        
    Returns:
        pd.DataFrame: DataFrame with moving averages for each period
    """
    ma_dict = {}
    
    for period in periods:
        ma_dict[f'MA_{period}'] = prices.rolling(window=period).mean()
    
    moving_averages = pd.DataFrame(ma_dict)
    
    return moving_averages

def calculate_stochastic_oscillator(data, k_period=14, d_period=3):
    """
    Calculate Stochastic Oscillator.
    
    Args:
        data (pd.DataFrame): DataFrame with High, Low, Close prices
        k_period (int): K period
        d_period (int): D period
        
    Returns:
        pd.DataFrame: DataFrame with %K and %D values
    """
    # Calculate %K
    low_min = data['Low'].rolling(window=k_period).min()
    high_max = data['High'].rolling(window=k_period).max()
    
    # Avoid division by zero
    denominator = high_max - low_min
    denominator = denominator.replace(0, 0.00001)
    
    k = 100 * ((data['Close'] - low_min) / denominator)
    
    # Calculate %D
    d = k.rolling(window=d_period).mean()
    
    # Create DataFrame with results
    stochastic = pd.DataFrame({
        'Stoch_K': k,
        'Stoch_D': d
    })
    
    return stochastic

def calculate_atr(data, period=14):
    """
    Calculate Average True Range (ATR).
    
    Args:
        data (pd.DataFrame): DataFrame with High, Low, Close prices
        period (int): ATR period
        
    Returns:
        pd.Series: ATR values
    """
    high = data['High']
    low = data['Low']
    close = data['Close']
    
    # Calculate True Range
    tr1 = high - low
    tr2 = abs(high - close.shift())
    tr3 = abs(low - close.shift())
    
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # Calculate ATR
    atr = tr.rolling(window=period).mean()
    
    return atr

def get_support_resistance(data, window=10):
    """
    Identify support and resistance levels.
    
    Args:
        data (pd.DataFrame): DataFrame with price data
        window (int): Window for local mins and maxs
        
    Returns:
        tuple: (support_levels, resistance_levels)
    """
    # Find local maximums and minimums
    data['Local_Min'] = data['Low'].rolling(window=(window*2)+1, center=True).min() == data['Low']
    data['Local_Max'] = data['High'].rolling(window=(window*2)+1, center=True).max() == data['High']
    
    # Get resistance levels (local highs)
    resistance_levels = data[data['Local_Max']]['High'].dropna().tolist()
    
    # Get support levels (local lows)
    support_levels = data[data['Local_Min']]['Low'].dropna().tolist()
    
    # Clean up
    del data['Local_Min']
    del data['Local_Max']
    
    return support_levels, resistance_levels