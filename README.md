# Real-Time Stock Analysis Application

A comprehensive stock analysis dashboard built with Streamlit and Python. This application provides real-time stock data visualization, technical analysis, and financial metrics to help users make informed investment decisions.

## Features

-  **Real-time Stock Data**: Access up-to-date market information using Yahoo Finance API
-  **Technical Analysis**: View RSI, MACD, Bollinger Bands, and Moving Averages
-  **Financial Analysis**: Calculate returns, volatility, and risk metrics
-  **Price Prediction**: Monte Carlo simulations for price forecasting
-  **News Feed**: Recent news related to the selected stock
-  **Responsive Design**: Works on desktop and mobile devices

## Installation

### Option 1: Traditional Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/stock-analysis-app.git
cd stock-analysis-app
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

### Option 2: Docker Setup (Recommended)

1. Clone this repository:
```bash
git clone https://github.com/yourusername/stock-analysis-app.git
cd stock-analysis-app
```

2. Build and run using Docker Compose:
```bash
docker-compose up -d
```

3. Access the application at http://localhost:8501

4. To stop the application:
```bash
docker-compose down
```

## Usage

1. Enter a stock symbol in the sidebar (e.g., AAPL, MSFT, GOOGL)
2. Select the time range and data interval
3. Choose which technical indicators to display
4. Navigate through the different tabs to access various analyses

## Customization

You can easily extend this application:

- Add new technical indicators in `technical_indicators.py`
- Create new visualization functions in `visualization.py`
- Implement more financial analysis methods in `analysis.py`
- Enhance the UI in `app.py`

## Dependencies

- Streamlit
- yfinance
- pandas
- numpy
- plotly
- scipy

## Deployment

### Docker Deployment

This application can be easily deployed using Docker:

1. Make sure you have Docker and Docker Compose installed
2. Run `docker-compose up -d` to start the application
3. Access the application at http://localhost:8501

For detailed deployment instructions, see the [Docker Deployment Instructions](Docker_Deployment_Instructions.md).

### CI/CD with GitHub Actions

The repository includes a GitHub Actions workflow for continuous integration and deployment:

1. Automatically runs tests on push/PR to main branch
2. Builds and tests the Docker image
3. Pushes the image to Docker Hub (on merge to main)

To set up CI/CD:
1. Fork this repository
2. Add your Docker Hub credentials as secrets in GitHub:
   - `DOCKER_HUB_USERNAME`
   - `DOCKER_HUB_TOKEN`

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This application is for educational purposes only. The financial analysis and predictions should not be considered as investment advice. Always conduct your own research before making investment decisions.
