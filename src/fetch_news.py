import os
import json
import time
from newsapi import NewsApiClient
from datetime import datetime, timedelta

def fetch_company_news(api_key, company_name, ticker, from_date, to_date, save_dir='data/raw'):
    """
    Fetches news articles for a specific company and saves them to a JSON file.
    """
    print(f"Fetching news for {company_name}...")
    try:
        newsapi = NewsApiClient(api_key=api_key)
        
        all_articles = newsapi.get_everything(
            q=company_name,
            from_param=from_date,
            to=to_date,
            language='en',
            sort_by='publishedAt'
        )
        
        if all_articles['totalResults'] == 0:
            print(f"Warning: No news articles found for {company_name}.")
            return

        filename = f"{ticker}_news.json"
        save_path = os.path.join(save_dir, filename)

        with open(save_path, 'w') as f:
            json.dump(all_articles, f, indent=4)
            
        print(f"✅ News for {company_name} saved to {save_path} ({all_articles['totalResults']} articles)")

    except Exception as e:
        print(f"❌ Failed to fetch news for {company_name}. Error: {e}")

if __name__ == '__main__':
    
    MY_API_KEY = "1017e27d41454b26bad24b3b1b3f4774"

    if MY_API_KEY == "PASTE_YOUR_API_KEY_HERE":
        print("Error: Please paste your News API key into the script.")
    else:
        companies = {
            "RELIANCE.NS": "Reliance Industries",
            "TCS.NS": "Tata Consultancy Services",
            "HDFCBANK.NS": "HDFC Bank",
            "INFY.NS": "Infosys",
            "ICICIBANK.NS": "ICICI Bank",
            "HINDUNILVR.NS": "Hindustan Unilever",
            "BHARTIARTL.NS": "Bharti Airtel",
            "ITC.NS": "ITC Limited",
            "SBIN.NS": "State Bank of India",
            "LT.NS": "Larsen & Toubro"
        }

        to_date_str = datetime.today().strftime('%Y-%m-%d')
        from_date_str = (datetime.today() - timedelta(days=28)).strftime('%Y-%m-%d')

        for ticker, name in companies.items():
            fetch_company_news(MY_API_KEY, name, ticker, from_date=from_date_str, to_date=to_date_str)
            time.sleep(1) 

        print("\n--- News fetching complete. ---")