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
            "ADANIENT.NS": "Adani Enterprises", "ADANIPORTS.NS": "Adani Ports",
            "APOLLOHOSP.NS": "Apollo Hospitals", "ASIANPAINT.NS": "Asian Paints",
            "AXISBANK.NS": "Axis Bank", "BAJAJ-AUTO.NS": "Bajaj Auto",
            "BAJFINANCE.NS": "Bajaj Finance", "BAJAJFINSV.NS": "Bajaj Finserv",
            "BPCL.NS": "Bharat Petroleum", "BHARTIARTL.NS": "Bharti Airtel",
            "BRITANNIA.NS": "Britannia Industries", "CIPLA.NS": "Cipla",
            "COALINDIA.NS": "Coal India", "DIVISLAB.NS": "Divi's Laboratories",
            "DRREDDY.NS": "Dr. Reddy's Laboratories", "EICHERMOT.NS": "Eicher Motors",
            "GRASIM.NS": "Grasim Industries", "HCLTECH.NS": "HCL Technologies",
            "HDFCBANK.NS": "HDFC Bank", "HDFCLIFE.NS": "HDFC Life",
            "HEROMOTOCO.NS": "Hero MotoCorp", "HINDALCO.NS": "Hindalco Industries",
            "HINDUNILVR.NS": "Hindustan Unilever", "ICICIBANK.NS": "ICICI Bank",
            "ITC.NS": "ITC Limited", "INDUSINDBK.NS": "IndusInd Bank",
            "INFY.NS": "Infosys", "JSWSTEEL.NS": "JSW Steel",
            "KOTAKBANK.NS": "Kotak Mahindra Bank", "LTIM.NS": "LTIMindtree",
            "LT.NS": "Larsen & Toubro", "M&M.NS": "Mahindra & Mahindra",
            "MARUTI.NS": "Maruti Suzuki", "NTPC.NS": "NTPC",
            "NESTLEIND.NS": "Nestle India", "ONGC.NS": "ONGC",
            "POWERGRID.NS": "Power Grid Corporation", "RELIANCE.NS": "Reliance Industries",
            "SBILIFE.NS": "SBI Life Insurance", "SBIN.NS": "State Bank of India",
            "SUNPHARMA.NS": "Sun Pharmaceutical", "TCS.NS": "Tata Consultancy Services",
            "TATACONSUM.NS": "Tata Consumer Products", "TATAMOTORS.NS": "Tata Motors",
            "TATASTEEL.NS": "Tata Steel", "TECHM.NS": "Tech Mahindra",
            "TITAN.NS": "Titan Company", "UPL.NS": "UPL",
            "ULTRACEMCO.NS": "UltraTech Cement", "WIPRO.NS": "Wipro"
        }

        to_date_str = datetime.today().strftime('%Y-%m-%d')
        from_date_str = (datetime.today() - timedelta(days=28)).strftime('%Y-%m-%d')

        for ticker, name in companies.items():
            fetch_company_news(MY_API_KEY, name, ticker, from_date=from_date_str, to_date=to_date_str)
            time.sleep(1)

        print("\n--- News fetching complete. ---")