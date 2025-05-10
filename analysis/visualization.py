import plotly.graph_objs as go
import pandas as pd
import numpy as np

def plot_candlestick(data):
    """
    Create a candlestick chart for stock data.
    
    Args:
        data (pd.DataFrame): DataFrame with OHLC data
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    # Add candlestick trace
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price'
    ))
    
    # Update layout
    fig.update_layout(
        title='Stock Price',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        height=500,
        margin=dict(l=0, r=0, t=30, b=0),
    )
    
    return fig

def plot_volume(data):
    """
    Create a volume chart for stock data.
    
    Args:
        data (pd.DataFrame): DataFrame with volume data
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    # Set colors based on price change
    colors = ['red' if data['Close'][i] < data['Open'][i] else 'green' for i in range(len(data))]
    
    # Add volume trace
    fig.add_trace(go.Bar(
        x=data.index,
        y=data['Volume'],
        marker_color=colors,
        name='Volume'
    ))
    
    # Update layout
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Volume',
        height=250,
        margin=dict(l=0, r=0, t=30, b=0),
    )
    
    return fig

def plot_indicators(data, indicator_type):
    """
    Create charts for various technical indicators.
    
    Args:
        data (pd.DataFrame): DataFrame with price and indicator data
        indicator_type (str): Type of indicator to plot
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    if indicator_type == 'bollinger':
        # Plot close price
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            name='Close',
            line=dict(color='blue', width=1)
        ))
        
        # Plot Bollinger Bands
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['BB_Upper'],
            name='Upper Band',
            line=dict(color='red', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['BB_Middle'],
            name='Middle Band',
            line=dict(color='orange', width=1)
        ))
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['BB_Lower'],
            name='Lower Band',
            line=dict(color='green', width=1)
        ))
        
        # Fill between upper and lower bands
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['BB_Upper'],
            fill=None,
            line=dict(color='rgba(0,0,0,0)')
        ))
        
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['BB_Lower'],
            fill='tonexty',
            fillcolor='rgba(173, 204, 255, 0.2)',
            line=dict(color='rgba(0,0,0,0)')
        ))
        
    elif indicator_type == 'ma':
        # Plot close price
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Close'],
            name='Close',
            line=dict(color='black', width=1)
        ))
        
        # Plot Moving Averages
        if 'MA20' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['MA20'],
                name='MA20',
                line=dict(color='blue', width=1.5)
            ))
        
        if 'MA50' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['MA50'],
                name='MA50',
                line=dict(color='orange', width=1.5)
            ))
        
        if 'MA200' in data.columns:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=data['MA200'],
                name='MA200',
                line=dict(color='red', width=1.5)
            ))
            
    # Update layout
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return fig

def plot_comparison(stocks_data, tickers):
    """
    Create a comparison chart for multiple stocks.
    
    Args:
        stocks_data (dict): Dictionary with stock data for each ticker
        tickers (list): List of ticker symbols
        
    Returns:
        go.Figure: Plotly figure object
    """
    fig = go.Figure()
    
    for ticker in tickers:
        # Normalize to percentage change from start
        norm_data = (stocks_data[ticker]['Close'] / stocks_data[ticker]['Close'].iloc[0] - 1) * 100
        
        fig.add_trace(go.Scatter(
            x=stocks_data[ticker].index,
            y=norm_data,
            name=ticker,
        ))
    
    # Update layout
    fig.update_layout(
        title='Comparison (% Change)',
        xaxis_title='Date',
        yaxis_title='Change (%)',
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
    )
    
    return fig

def plot_correlation_matrix(stocks_data, tickers):
    """
    Create a correlation matrix heatmap for multiple stocks.
    
    Args:
        stocks_data (dict): Dictionary with stock data for each ticker
        tickers (list): List of ticker symbols
        
    Returns:
        go.Figure: Plotly figure object
    """
    # Create DataFrame for correlation matrix
    returns_data = pd.DataFrame()
    
    for ticker in tickers:
        returns_data[ticker] = stocks_data[ticker]['Close'].pct_change().dropna()
    
    # Calculate correlation matrix
    corr_matrix = returns_data.corr()
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=tickers,
        y=tickers,
        colorscale='RdBu_r',
        zmin=-1,
        zmax=1,
        text=np.round(corr_matrix.values, 2),
        texttemplate="%{text}",
    ))
    
    # Update layout
    fig.update_layout(
        title='Correlation Matrix',
        height=400,
        margin=dict(l=0, r=0, t=30, b=0),
    )
    
    return fig