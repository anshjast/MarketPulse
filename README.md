# MarketPulse

MarketPulse is a Python-powered application that predicts the next day's stock trend for select NIFTY 50 companies using a combination of price action, technical indicators, and real-time news sentiment analysis.

## Features

- **Stock Trend Prediction:** Predicts whether the stock price will go up or down for NIFTY 50 companies.
- **Technical Indicators:** Computes and uses features like SMA (Simple Moving Average), RSI (Relative Strength Index), MACD, and Bollinger Bands.
- **News Sentiment Analysis:** Fetches company news using the NewsAPI and analyzes headline sentiment to improve prediction accuracy.
- **Data Pipeline:** Automated fetching and processing of stock prices and news, building datasets, and training machine learning models.
- **Web Interface:** Built with Streamlit for interactive usage.

## How It Works

1. **Fetch Stock Data:** Downloads historical stock price data for selected companies using Yahoo Finance.
2. **Fetch News:** Retrieves recent news articles for each company using NewsAPI.
3. **Process Sentiment:** Analyzes news headlines to calculate a daily sentiment score.
4. **Build Dataset:** Merges price data, technical indicators, and sentiment scores into a unified dataset.
5. **Model Training:** Trains an XGBoost classifier with hyperparameter tuning to predict next-day stock movement.
6. **Web App:** Users select a company, and the model predicts the next day's trend based on the latest available data.

## Setup Instructions

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [pandas](https://pandas.pydata.org/)
- [yfinance](https://pypi.org/project/yfinance/)
- [newsapi-python](https://github.com/mattlisiv/newsapi-python)
- [nltk](https://www.nltk.org/)
- [scikit-learn](https://scikit-learn.org/)
- [xgboost](https://xgboost.readthedocs.io/)
- [joblib](https://joblib.readthedocs.io/)

Install dependencies:

```bash
pip install -r requirements.txt
```

### Data Collection & Preprocessing

1. **Fetch Stock Prices:**
   ```bash
   python src/fetch_stock_prices.py
   ```
2. **Fetch News Articles:**
   - Add your NewsAPI key to `src/fetch_news.py`.
   ```bash
   python src/fetch_news.py
   ```
3. **Process Sentiment:**
   ```bash
   python src/process_sentiment.py
   ```
4. **Build Dataset:**
   ```bash
   python src/build_dataset.py
   ```

### Model Training

```bash
python src/train_model.py
```

This will save the trained model as `models/marketpulse_classifier.joblib`.

### Running the Web App

1. Add your NewsAPI key to `app.py` (replace `"PASTE_YOUR_API_KEY_HERE"`).
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

- Use the web interface to select a NIFTY 50 company.
- Click "Predict Next Day Trend" to view the prediction and probability.

## Project Structure

```
.
├── app.py
├── src/
│   ├── fetch_stock_prices.py
│   ├── fetch_news.py
│   ├── process_sentiment.py
│   ├── build_dataset.py
│   └── train_model.py
├── models/
├── data/
│   ├── raw/
│   └── processed/
└── requirements.txt
```

## Notes

- You must provide your own NewsAPI key for news fetching and sentiment analysis.
- The project is designed for educational purposes and is not intended for real trading.

## License

This project is currently not licensed.

## Author

[anshjast](https://github.com/anshjast)
```
