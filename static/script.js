// static/script.js

const chartManager = {
    instance: null,
    container: document.getElementById('chart-container'),
    draw(labels, actualData, predictedData) {
        if (this.instance) {
            this.instance.destroy();
        }
        const ctx = document.getElementById('chart').getContext('2d');
        this.instance = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Actual Price (Test Data)',
                    data: actualData,
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.1
                }, {
                    label: 'Predicted Trend Line',
                    data: predictedData,
                    borderColor: 'rgb(255, 99, 71)',
                    borderWidth: 4,
                    pointRadius: 0,
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: { display: true, text: 'Model Performance on Test Data', font: { size: 18 } }
                },
                scales: {
                    x: { title: { display: true, text: 'Date' } },
                    y: { title: { display: true, text: 'Closing Price (USD)' } }
                }
            }
        });
        this.show();
    },
    hide() { this.container.style.display = 'none'; },
    show() { this.container.style.display = 'block'; }
};


async function fetchPrediction() {
    const tickerInput = document.getElementById('ticker');
    const predictBtn = document.getElementById('predictBtn');
    const resultTitle = document.getElementById('result-title');
    const errorDiv = document.getElementById('error-message');
    const ticker = tickerInput.value.trim().toUpperCase();

    if (!ticker) {
        errorDiv.textContent = 'Please enter a ticker symbol.';
        return;
    }

    predictBtn.disabled = true;
    predictBtn.textContent = 'Processing...';
    resultTitle.textContent = '';
    errorDiv.textContent = '';
    chartManager.hide();

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ticker })
        });

        const data = await response.json();

        // --- DEBUGGING STEP 1 ---
        // This will print the full received data object to the browser console.
        console.log("--- DEBUG: Data received by JavaScript from server ---");
        console.log(data);
        console.log("-------------------------------------------------");

        if (!response.ok) {
            throw new Error(data.error || 'An unknown server error occurred.');
        }
        
        // --- DEBUGGING STEP 2 ---
        // Explicitly check if the predicted array is missing or empty.
        if (!data.predicted || data.predicted.length === 0) {
            throw new Error("The server returned no prediction data points. The red line cannot be drawn.");
        }

        resultTitle.textContent = `Showing prediction results for ${ticker}`;
        chartManager.draw(data.dates, data.actual, data.predicted);

    } catch (error) {
        errorDiv.textContent = `Error: ${error.message}`;
    } finally {
        predictBtn.disabled = false;
        predictBtn.textContent = 'Get Prediction';
    }
}