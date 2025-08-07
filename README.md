# 📈 Stock Price Prediction Web App

This is a simple yet effective web-based **Stock Price Prediction System** built using **Linear Regression** in Python. The app uses a Flask backend and a responsive HTML/CSS/JavaScript frontend. It predicts stock prices based on historical data and displays both numerical output and a graphical chart.

---

## 🚀 Features

- 🔢 Predicts future stock prices using Linear Regression
- 📊 Displays prediction chart with actual and predicted values
- 🌐 Clean, responsive frontend with interactive design
- ⚙️ Flask-based backend for handling predictions
- 📦 Simple file structure for easy deployment

---

## 🛠️ Technologies Used

### Backend:
- Python 3
- Flask
- scikit-learn
- pandas
- matplotlib (optional for saving charts)

### Frontend:
- HTML5
- CSS3
- JavaScript (vanilla)
- Chart.js (for chart rendering)

---

## 📁 Project Structure
│
├── static/
│ ├── style.css # Styling for frontend
│ └── script.js # JS logic for fetching predictions & rendering chart
│
├── templates/
│ └── index.html # Main HTML page
│
├── model/
│ └── model.pkl # Trained Linear Regression model (Pickle)
│
├── main.py # Flask application
├── train_model.py # Model training script (optional)
├── requirements.txt # Python dependencies
└── README.md # You're here!
# stock-price-prediction
