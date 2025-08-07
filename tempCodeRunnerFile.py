from flask import Flask, render_template, request, jsonify
from model import get_stock_prediction

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    ticker = request.json['ticker']
    predictions = get_stock_prediction(ticker)
    return jsonify(predictions)

if __name__ == '__main__':
    app.run(debug=True)
