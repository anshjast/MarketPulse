import streamlit as st
import pandas as pd
import joblib
import yfinance as yf
from newsapi import NewsApiClient
from datetime import datetime, timedelta
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

model = joblib.load('models/marketpulse_classifier.joblib')

try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    st.write("Downloading VADER lexicon for sentiment analysis...")
    nltk.download('vader_lexicon')

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

def calculate_macd(data, slow=26, fast=12, signal=9):
    exp1 = data['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_bbands(data, length=20, std_dev=2):
    sma = data['Close'].rolling(window=length).mean()
    std = data['Close'].rolling(window=length).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band, lower_band

@st.cache_data(ttl=3600)
def get_prediction(ticker, company_name, api_key):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=90)
    price_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    if price_data.empty:
        return "Error: Could not fetch price data.", None

    newsapi = NewsApiClient(api_key=api_key)
    news_end_date = end_date.strftime('%Y-%m-%d')
    news_start_date = (end_date - timedelta(days=1)).strftime('%Y-%m-%d')
    articles = newsapi.get_everything(q=company_name, from_param=news_start_date, to=news_end_date, language='en')

    sia = SentimentIntensityAnalyzer()
    sentiment_score = 0.0
    if articles['totalResults'] > 0:
        scores = [sia.polarity_scores(article['title'])['compound'] for article in articles['articles'] if article['title']]
        if scores:
            sentiment_score = sum(scores) / len(scores)

    price_data['SMA_20'] = calculate_sma(price_data)
    price_data['RSI_14'] = calculate_rsi(price_data)
    price_data['MACD'], price_data['MACD_Signal'] = calculate_macd(price_data)
    price_data['Upper_Band'], price_data['Lower_Band'] = calculate_bbands(price_data)
    
    latest_data = price_data.dropna().iloc[-1]
    
    features = pd.DataFrame({
        'Open': [latest_data['Open']], 'High': [latest_data['High']],
        'Low': [latest_data['Low']], 'Close': [latest_data['Close']],
        'Volume': [latest_data['Volume']], 'sentiment_score': [sentiment_score],
        'SMA_20': [latest_data['SMA_20']], 'RSI_14': [latest_data['RSI_14']],
        'MACD': [latest_data['MACD']], 'MACD_Signal': [latest_data['MACD_Signal']],
        'Upper_Band': [latest_data['Upper_Band']], 'Lower_Band': [latest_data['Lower_Band']]
    })

    model_features = ['Open', 'High', 'Low', 'Close', 'Volume', 'sentiment_score', 'SMA_20', 'RSI_14', 'MACD', 'MACD_Signal', 'Upper_Band', 'Lower_Band']
    features = features[model_features]
    features = features.astype(float)

    prediction = model.predict(features)
    probability = model.predict_proba(features)
    
    return prediction, probability

st.title('MarketPulse India 🇮🇳')
st.write("Predicts the next day's stock trend for select NIFTY 50 companies.")

MY_API_KEY = "1017e27d41454b26bad24b3b1b3f4774"

companies = {
    "ADANIENT.NS": "Adani Enterprises", "ADANIPORTS.NS": "Adani Ports", "APOLLOHOSP.NS": "Apollo Hospitals",
    "ASIANPAINT.NS": "Asian Paints", "AXISBANK.NS": "Axis Bank", "BAJAJ-AUTO.NS": "Bajaj Auto",
    "BAJFINANCE.NS": "Bajaj Finance", "BAJAJFINSV.NS": "Bajaj Finserv", "BPCL.NS": "Bharat Petroleum",
    "BHARTIARTL.NS": "Bharti Airtel", "BRITANNIA.NS": "Britannia Industries", "CIPLA.NS": "Cipla",
    "COALINDIA.NS": "Coal India", "DIVISLAB.NS": "Divi's Laboratories", "DRREDDY.NS": "Dr. Reddy's Laboratories",
    "EICHERMOT.NS": "Eicher Motors", "GRASIM.NS": "Grasim Industries", "HCLTECH.NS": "HCL Technologies",
    "HDFCBANK.NS": "HDFC Bank", "HDFCLIFE.NS": "HDFC Life", "HEROMOTOCO.NS": "Hero MotoCorp",
    "HINDALCO.NS": "Hindalco Industries", "HINDUNILVR.NS": "Hindustan Unilever", "ICICIBANK.NS": "ICICI Bank",
    "ITC.NS": "ITC Limited", "INDUSINDBK.NS": "IndusInd Bank", "INFY.NS": "Infosys",
    "JSWSTEEL.NS": "JSW Steel", "KOTAKBANK.NS": "Kotak Mahindra Bank", "LTIM.NS": "LTIMindtree",
    "LT.NS": "Larsen & Toubro", "M&M.NS": "Mahindra & Mahindra", "MARUTI.NS": "Maruti Suzuki",
    "NTPC.NS": "NTPC", "NESTLEIND.NS": "Nestle India", "ONGC.NS": "ONGC",
    "POWERGRID.NS": "Power Grid Corporation", "RELIANCE.NS": "Reliance Industries", "SBILIFE.NS": "SBI Life Insurance",
    "SBIN.NS": "State Bank of India", "SUNPHARMA.NS": "Sun Pharmaceutical", "TCS.NS": "Tata Consultancy Services",
    "TATACONSUM.NS": "Tata Consumer Products", "TATAMOTORS.NS": "Tata Motors", "TATASTEEL.NS": "Tata Steel",
    "TECHM.NS": "Tech Mahindra", "TITAN.NS": "Titan Company", "UPL.NS": "UPL",
    "ULTRACEMCO.NS": "UltraTech Cement", "WIPRO.NS": "Wipro"
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