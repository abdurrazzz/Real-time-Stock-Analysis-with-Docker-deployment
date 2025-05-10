import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import plotly.graph_objs as go
from data.technical_data import calculate_rsi, calculate_macd, calculate_bollinger_bands
from utils.market_data import get_stock_data, get_company_info, get_news
from analysis.visualization import plot_candlestick, plot_volume, plot_indicators
from analysis.analysis import calculate_returns, calculate_volatility, perform_monte_carlo

# Set page config
st.set_page_config(
    page_title="Stock Analysis Dashboard",
    page_icon="📈",
    layout="wide"
)

# App title and description
st.title("Real-Time Stock Analysis Dashboard")
st.markdown("""
This application provides real-time stock analysis, technical indicators, and visualization tools.
Enter a stock symbol to get started.
""")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    ticker_symbol = st.text_input("Enter Stock Symbol", "AAPL").upper()
    
    start_date = st.date_input(
        "Start Date",
        datetime.date.today() - datetime.timedelta(days=365)
    )
    
    end_date = st.date_input(
        "End Date",
        datetime.date.today()
    )
    
    interval = st.selectbox(
        "Interval",
        options=["1d", "1h", "15m", "5m", "1m"],
        index=0
    )
    
    indicators = st.multiselect(
        "Select Technical Indicators",
        ["RSI", "MACD", "Bollinger Bands", "Moving Averages"],
        default=["RSI", "MACD"]
    )
    
    analysis_period = st.slider(
        "Analysis Period (days)",
        min_value=7,
        max_value=365,
        value=30
    )
    
    st.button("Refresh Data", key="refresh")

# Get stock data
try:
    with st.spinner(f"Loading data for {ticker_symbol}..."):
        # Get stock data
        stock_data = get_stock_data(ticker_symbol, start_date, end_date, interval)
        
        # Get company info
        company_info = get_company_info(ticker_symbol)
        
        # Main layout - use tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Technical Analysis", "Financial Analysis", "News"])
        
        # Tab 1: Overview
        with tab1:
            # Company info
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if 'logo_url' in company_info and company_info['logo_url']:
                    st.image(company_info['logo_url'], width=100)
                st.subheader(f"{company_info['name']} ({ticker_symbol})")
                st.metric("Current Price", f"${stock_data['Close'].iloc[-1]:.2f}", 
                          f"{((stock_data['Close'].iloc[-1] / stock_data['Close'].iloc[-2]) - 1) * 100:.2f}%")
                st.metric("Volume", f"{stock_data['Volume'].iloc[-1]:,.0f}")
                
            with col2:
                st.subheader("Company Information")
                st.write(company_info['description'])
                st.write(f"Sector: {company_info['sector']}")
                st.write(f"Industry: {company_info['industry']}")
                st.write(f"Website: {company_info['website']}")
            
            # Stock price chart
            st.subheader("Stock Price")
            fig = plot_candlestick(stock_data)
            st.plotly_chart(fig, use_container_width=True)
            
            # Volume chart
            st.subheader("Trading Volume")
            volume_fig = plot_volume(stock_data)
            st.plotly_chart(volume_fig, use_container_width=True)
        
        # Tab 2: Technical Analysis
        with tab2:
            st.subheader("Technical Indicators")
            
            # Calculate technical indicators
            if "RSI" in indicators:
                stock_data['RSI'] = calculate_rsi(stock_data['Close'])
                
                st.subheader("Relative Strength Index (RSI)")
                fig_rsi = go.Figure()
                fig_rsi.add_trace(go.Scatter(x=stock_data.index, y=stock_data['RSI'], name="RSI"))
                fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought")
                fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold")
                fig_rsi.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_rsi, use_container_width=True)
            
            if "MACD" in indicators:
                macd_data = calculate_macd(stock_data['Close'])
                stock_data = pd.concat([stock_data, macd_data], axis=1)
                
                st.subheader("Moving Average Convergence Divergence (MACD)")
                fig_macd = go.Figure()
                fig_macd.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD'], name="MACD"))
                fig_macd.add_trace(go.Scatter(x=stock_data.index, y=stock_data['MACD_Signal'], name="Signal"))
                fig_macd.add_trace(go.Bar(x=stock_data.index, y=stock_data['MACD_Hist'], name="Histogram"))
                fig_macd.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_macd, use_container_width=True)
            
            if "Bollinger Bands" in indicators:
                bollinger = calculate_bollinger_bands(stock_data['Close'])
                stock_data = pd.concat([stock_data, bollinger], axis=1)
                
                st.subheader("Bollinger Bands")
                fig_bb = plot_indicators(stock_data, 'bollinger')
                st.plotly_chart(fig_bb, use_container_width=True)
            
            if "Moving Averages" in indicators:
                stock_data['MA20'] = stock_data['Close'].rolling(window=20).mean()
                stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
                stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()
                
                st.subheader("Moving Averages")
                fig_ma = plot_indicators(stock_data, 'ma')
                st.plotly_chart(fig_ma, use_container_width=True)
        
        # Tab 3: Financial Analysis
        with tab3:
            st.subheader("Financial Analysis")
            
            # Returns calculation
            returns = calculate_returns(stock_data['Close'])
            volatility = calculate_volatility(returns)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Daily Returns (Avg)", f"{returns.mean() * 100:.2f}%")
                st.metric("Annualized Return", f"{returns.mean() * 252 * 100:.2f}%")
                
                # Distribution of returns
                st.subheader("Returns Distribution")
                fig_dist = go.Figure()
                fig_dist.add_trace(go.Histogram(x=returns, nbinsx=50, name="Daily Returns"))
                fig_dist.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_dist, use_container_width=True)
            
            with col2:
                st.metric("Volatility (Daily)", f"{volatility * 100:.2f}%")
                st.metric("Volatility (Annualized)", f"{volatility * np.sqrt(252) * 100:.2f}%")
                
                # Cumulative returns
                st.subheader("Cumulative Returns")
                cum_returns = (1 + returns).cumprod() - 1
                fig_cum = go.Figure()
                fig_cum.add_trace(go.Scatter(x=cum_returns.index, y=cum_returns, fill='tozeroy', name="Cumulative Returns"))
                fig_cum.update_layout(height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_cum, use_container_width=True)
            
            # Monte Carlo simulation
            st.subheader("Monte Carlo Simulation (Next 30 days)")
            mc_results = perform_monte_carlo(stock_data['Close'].iloc[-1], returns, days=30, simulations=100)
            
            fig_mc = go.Figure()
            for i in range(mc_results.shape[1]):
                fig_mc.add_trace(go.Scatter(x=np.arange(0, 31), y=mc_results.iloc[:, i], 
                                            line=dict(width=0.5), opacity=0.3, name=f"Sim {i+1}"))
            
            # Add mean line
            mean_line = mc_results.mean(axis=1)
            fig_mc.add_trace(go.Scatter(x=np.arange(0, 31), y=mean_line, 
                                        line=dict(color='red', width=2), name="Mean"))
            
            fig_mc.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_mc, use_container_width=True)
            
            # Final day distribution
            final_day = mc_results.iloc[-1]
            pct_change = (final_day / stock_data['Close'].iloc[-1] - 1) * 100
            
            st.metric("Expected Price (30 days)", f"${mean_line.iloc[-1]:.2f}", 
                      f"{(mean_line.iloc[-1] / stock_data['Close'].iloc[-1] - 1) * 100:.2f}%")
            
            st.subheader("Forecasted Price Distribution (30 days)")
            fig_dist = go.Figure()
            fig_dist.add_trace(go.Histogram(x=pct_change, nbinsx=50))
            fig_dist.update_layout(height=300, xaxis_title="% Change from Current Price")
            st.plotly_chart(fig_dist, use_container_width=True)
        
        # Tab 4: News
        with tab4:
            st.subheader(f"Recent News for {ticker_symbol}")
            
            news = get_news(ticker_symbol)
            
            if news:
                for article in news:
                    with st.expander(f"{article['title']} ({article['published_date']})"):
                        st.write(article['summary'])
                        st.write(f"Source: {article['source']}")
                        st.write(f"[Read more]({article['url']})")
            else:
                st.write("No recent news found.")

except Exception as e:
    st.error(f"Error: {e}")
    st.error("Please check the stock symbol and try again.")