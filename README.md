# 📘 MarketPulse

A data-driven stock trend prediction application combining technical indicators, news sentiment, and machine learning.

## 🚀 Overview

MarketPulse is a Streamlit-based application that predicts the next-day stock trend for selected NIFTY 50 companies.

It demonstrates how multiple data sources (market prices + news sentiment) can be ingested, processed, and converted into actionable signals using feature engineering and machine learning.

## 🧠 What This Project Demonstrates

API-driven data ingestion

Feature engineering with technical indicators

NLP-based sentiment analysis

ML-based prediction pipeline

End-to-end data → insight → UI workflow

## 🏗️ System Architecture
## 🏗️ System Architecture

```text
[Yahoo Finance API]        [News API]
        |                      |
        v                      v
 Market Price Data     News Sentiment Data
        |                      |
        +----------+-----------+
                   |
                   v
     Feature Engineering + ML Model
                   |
                   v
            Streamlit Web App
```



## ⚙️ Tech Stack

Frontend: Streamlit

Data Sources: yFinance, NewsAPI

Machine Learning: Scikit-learn (joblib)

NLP: NLTK (VADER Sentiment Analyzer)

Language: Python

## ✨ Key Features

Predicts next-day stock trend (Up / Down)

Uses technical indicators:

SMA

RSI

MACD

Bollinger Bands

Incorporates real-time news sentiment

Displays prediction confidence

Simple interactive UI

## ▶️ How to Run
1. Install dependencies
pip install streamlit pandas yfinance newsapi-python nltk joblib scikit-learn

2. Add your News API key
MY_API_KEY = "YOUR_NEWS_API_KEY"

3. Run the application
streamlit run app.py

## 📦 Sample Prediction Output
### 📦 Sample Prediction Output

```text
Prediction: Likely to go UP
Confidence: 78.4%
```

```text
Prediction: Likely to go DOWN or stay the same
Confidence: 64.2%
```


## 📈 Why This Matters

This project mirrors real-world systems where:

Multiple APIs feed raw signals

Data is transformed into structured features

Models generate probabilistic outcomes

Results are surfaced through simple interfaces

These patterns are common in analytics platforms, GTM systems, and decision-support tools.

## 🔮 Possible Enhancements

Model retraining pipeline

Historical prediction tracking

Advanced NLP models

Cloud deployment

## 👤 Author

Ansh Jast
