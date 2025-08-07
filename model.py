# model.py

import logging
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from typing import Dict, Any

def get_stock_prediction(ticker: str) -> Dict[str, Any]:
    """
    Downloads historical stock data, splits it, trains a linear regression model,
    and returns test data predictions.
    """
    logging.info(f"Starting prediction process for ticker: {ticker}")
    try:
        data = yf.download(ticker, start="2020-01-01", end="2024-12-31", progress=False, auto_adjust=True)
        data.dropna(inplace=True)

        if data.empty:
            logging.warning(f"No data downloaded for ticker: {ticker}.")
            return {"error": f"No data found for ticker '{ticker}'. Please check the symbol."}

        data = data[['Close']].reset_index()
        data['Date_ordinal'] = data['Date'].map(pd.Timestamp.toordinal)

        X = data[['Date_ordinal']]
        y = data['Close']

        if len(X) < 20:
            logging.warning(f"Insufficient data for {ticker} (less than 20 data points).")
            return {"error": f"Not enough historical data for '{ticker}' to create a prediction."}

        split_index = int(len(X) * 0.8)
        X_train, X_test = X[:split_index], X[split_index:]
        y_train, y_test = y[:split_index], y[split_index:]

        if X_test.empty:
            logging.warning(f"Test set for {ticker} is empty after split.")
            return {"error": f"Not enough recent data for '{ticker}' to form a valid test set."}

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        test_dates = data.loc[X_test.index, 'Date']
        actual_prices = y_test.squeeze().tolist()
        
        # Prepare the final dictionary
        result = {
            'dates': test_dates.dt.strftime('%Y-%m-%d').tolist(),
            'actual': actual_prices,
            
            # --- THE DEFINITIVE FIX IS HERE ---
            # Flatten the 2D numpy array (e.g., [[1], [2]]) into a 1D list (e.g., [1, 2])
            # This is the format that Chart.js requires.
            'predicted': y_pred.flatten().tolist()
        }

        # You can remove the debug print statements now if you wish
        print("--- DEBUG: Final dictionary being returned from model.py ---")
        print(f"Number of predicted points: {len(result['predicted'])}")
        print(f"First 5 predicted points: {result['predicted'][:5]}")
        print("----------------------------------------------------------")

        return result

    except Exception as e:
        logging.error(f"An unexpected error occurred in get_stock_prediction for {ticker}: {e}")
        return {"error": "An internal server error occurred while processing the data."}