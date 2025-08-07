# app.py

import logging
from flask import Flask, render_template, request, jsonify
from model import get_stock_prediction # Import the model function

# Configure logging for better server-side debugging.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/')
def index():
    """Renders the main HTML page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint to handle prediction requests."""
    # Ensure the request is in the expected JSON format.
    if not request.is_json:
        return jsonify({"error": "Invalid request: Content-Type must be application/json"}), 415

    try:
        data = request.get_json()
        ticker = data.get('ticker')

        # Validate the input ticker.
        if not ticker or not isinstance(ticker, str):
            return jsonify({"error": "Ticker symbol must be a non-empty string."}), 400

        # Sanitize ticker input.
        ticker = ticker.strip().upper()
        logging.info(f"Received prediction request for ticker: {ticker}")
        
        # Call the separated model function to get predictions.
        prediction_result = get_stock_prediction(ticker)

        # Handle potential errors returned from the model function.
        if "error" in prediction_result:
            # 404 is appropriate for "not found" type errors (e.g., invalid ticker).
            return jsonify(prediction_result), 404
            
        # On success, return the prediction data with a 200 OK status.
        return jsonify(prediction_result), 200

    except Exception as e:
        logging.error(f"An unhandled error occurred in the /predict endpoint: {e}")
        return jsonify({"error": "An unexpected internal server error occurred."}), 500

if __name__ == '__main__':
    # For production, use a proper WSGI server like Gunicorn or uWSGI.
    app.run(debug=True)