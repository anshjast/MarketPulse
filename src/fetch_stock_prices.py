import yfinance as yf
import os
import time
from datetime import datetime

def fetch_stock_data(ticker, start_date='2020-01-01', end_date=None, save_dir='data/raw'):
    """
    Fetches historical stock data from Yahoo Finance and saves it as a CSV file.
    """
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')

    os.makedirs(save_dir, exist_ok=True)
    
    print(f"Fetching data for {ticker} from {start_date} to {end_date}...")
    
    try:
        stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if stock_data.empty:
            print(f"Warning: No data returned for {ticker}.")
            return

        filename = f"{ticker}.csv"
        save_path = os.path.join(save_dir, filename)
        stock_data.reset_index(inplace=True)
        stock_data.to_csv(save_path, index=False)
        print(f"✅ Data for {ticker} saved to {save_path}")

    except Exception as e:
        print(f"❌ Failed to download data for {ticker}. Error: {e}")

if __name__ == '__main__':
    nifty50_tickers = [
        "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
        "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BPCL.NS", "BHARTIARTL.NS",
        "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
        "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
        "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "ITC.NS",
        "INDUSINDBK.NS", "INFY.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LTIM.NS",
        "LT.NS", "M&M.NS", "MARUTI.NS", "NTPC.NS", "NESTLEIND.NS", "ONGC.NS",
        "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SUNPHARMA.NS",
        "TCS.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TECHM.NS",
        "TITAN.NS", "UPL.NS", "ULTRACEMCO.NS", "WIPRO.NS"
    ]
    
    for ticker in nifty50_tickers:
        fetch_stock_data(ticker)
        time.sleep(1) 
        
    print("\n--- Stock price data fetching complete. ---")