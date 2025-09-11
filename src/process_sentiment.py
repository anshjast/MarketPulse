import os
import json
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentiment(news_json_path, save_dir='data/processed'):
    """
    Analyzes the sentiment of news headlines from a JSON file and saves the
    daily average sentiment as a CSV.
    """
    ticker = os.path.basename(news_json_path).replace('_news.json', '')
    print(f"Analyzing sentiment for {ticker}...")
    
    try:
        with open(news_json_path, 'r') as f:
            news_data = json.load(f)
        
        if not news_data['articles']:
            print(f"Warning: No articles to analyze for {ticker}.")
            return
            
        sia = SentimentIntensityAnalyzer()
        
        sentiments = []
        for article in news_data['articles']:
            if article.get('title') and article.get('publishedAt'):
                score = sia.polarity_scores(article['title'])['compound']
                date = pd.to_datetime(article['publishedAt']).date()
                sentiments.append({'date': date, 'sentiment': score})

        if not sentiments:
            print(f"Warning: Could not extract any valid sentiment data for {ticker}.")
            return

        sentiment_df = pd.DataFrame(sentiments)
        
        daily_sentiment = sentiment_df.groupby('date')['sentiment'].mean().reset_index()
        daily_sentiment.rename(columns={'sentiment': 'sentiment_score'}, inplace=True)
        
        os.makedirs(save_dir, exist_ok=True)
        filename = f"{ticker}_sentiment.csv"
        save_path = os.path.join(save_dir, filename)
        daily_sentiment.to_csv(save_path, index=False)
        print(f"✅ Daily sentiment for {ticker} saved to {save_path}")

    except Exception as e:
        print(f"❌ Failed to process sentiment for {ticker}. Error: {e}")

if __name__ == '__main__':

    try:
        nltk.data.find('sentiment/vader_lexicon.zip')
    except LookupError:
        print("VADER lexicon not found. Downloading...")
        nltk.download('vader_lexicon')

    raw_data_dir = 'data/raw'
    news_files = [f for f in os.listdir(raw_data_dir) if f.endswith('_news.json')]
    
    for news_file in news_files:
        file_path = os.path.join(raw_data_dir, news_file)
        analyze_sentiment(file_path)
        
    print("\n--- Sentiment analysis complete. ---")