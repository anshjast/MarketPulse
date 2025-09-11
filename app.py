import streamlit as st
import pandas as pd
import joblib
import yfinance as yf
from newsapi import NewsApiClient
from datetime import datetime, timedelta
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# --- Load Model and VADER Lexicon ---
# Load your trained model
model = joblib.load('models/marketpulse_classifier.joblib')

# Download the VADER lexicon if it's not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    st.write("Downloading VADER lexicon for sentiment analysis...")
    nltk.download('vader_lexicon')

# --- Helper Functions ---
def calculate_sma(data, length=20):
    return data['Close'].rolling(window=length).mean()

def calculate_rsi(data, length=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    rs = gain / loss
    rs.fillna(0, inplace=True)
    rsi = 100 - (100 / (1 + rs))
    return rsi

# --- Main Prediction Function ---
@st.cache_data(ttl=3600) # Cache the result for 1 hour
def get_prediction(ticker, company_name, api_key):
    """Fetches live data, calculates features, and makes a prediction."""
    
    # 1. Fetch latest price data
    end_date = datetime.today()
    start_date = end_date - timedelta(days=60)
    price_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if price_data.empty:
        return "Error: Could not fetch price data.", None

    # 2. Fetch latest news data
    newsapi = NewsApiClient(api_key=api_key)
    news_end_date = end_date.strftime('%Y-%m-%d')
    news_start_date = (end_date - timedelta(days=1)).strftime('%Y-%m-%d')
    
    articles = newsapi.get_everything(
        q=company_name, from_param=news_start_date, to=news_end_date, language='en'
    )

    # 3. Calculate sentiment score
    sia = SentimentIntensityAnalyzer()
    sentiment_score = 0.0
    if articles['totalResults'] > 0:
        scores = [sia.polarity_scores(article['title'])['compound'] for article in articles['articles'] if article['title']]
        if scores:
            sentiment_score = sum(scores) / len(scores)

    # 4. Calculate technical indicators
    price_data['SMA_20'] = calculate_sma(price_data)
    price_data['RSI_14'] = calculate_rsi(price_data)
    
    # 5. Assemble the final feature vector for the model
    latest_data = price_data.dropna().iloc[-1]
    
    features = pd.DataFrame({
        'Open': [latest_data['Open']], 'High': [latest_data['High']],
        'Low': [latest_data['Low']], 'Close': [latest_data['Close']],
        'Volume': [latest_data['Volume']], 'sentiment_score': [sentiment_score],
        'SMA_20': [latest_data['SMA_20']], 'RSI_14': [latest_data['RSI_14']]
    })

    # --- NEW FIX: Ensure data types and column order are correct ---
    model_features = ['Open', 'High', 'Low', 'Close', 'Volume', 'sentiment_score', 'SMA_20', 'RSI_14']
    features = features[model_features] # Enforce column order
    features = features.astype(float) # Ensure all columns are numeric
    # --- End of Fix ---

    # 6. Make the prediction
    prediction = model.predict(features)
    probability = model.predict_proba(features)
    
    return prediction, probability

# --- Streamlit App ---

st.title('MarketPulse India 🇮🇳')
st.write("Predicts the next day's stock trend for select NIFTY 50 companies.")

# --- User Input ---
MY_API_KEY = "1017e27d41454b26bad24b3b1b3f4774"

companies = {
    "RELIANCE.NS": "Reliance Industries", "TCS.NS": "Tata Consultancy Services", 
    "HDFCBANK.NS": "HDFC Bank", "INFY.NS": "Infosys", "ICICIBANK.NS": "ICICI Bank",
    "HINDUNILVR.NS": "Hindustan Unilever", "BHARTIARTL.NS": "Bharti Airtel",
    "ITC.NS": "ITC Limited", "SBIN.NS": "State Bank of India", "LT.NS": "Larsen & Toubro"
}

ticker_selection = st.selectbox('Select a Company', options=list(companies.keys()), format_func=lambda x: companies[x])

if st.button('Predict Next Day Trend'):
    if MY_API_KEY == "PASTE_YOUR_API_KEY_HERE":
        st.error("Please add your News API key to the script to run the prediction.")
    else:
        with st.spinner(f"Analyzing latest data for {companies[ticker_selection]}..."):
            prediction, probability = get_prediction(ticker_selection, companies[ticker_selection], MY_API_KEY)

            if isinstance(prediction, str):
                st.error(prediction)
            else:
                if prediction[0] == 1:
                    st.subheader('Prediction: 📈 Likely to go UP')
                    confidence = probability[0][1]
                else:
                    st.subheader('Prediction: 📉 Likely to go DOWN or stay the same')
                    confidence = probability[0][0]

                st.write(f"**Confidence:** {confidence:.2%}")
                st.info("Disclaimer: This is an experimental prediction and not financial advice.", icon="⚠️")