import pandas as pd
import os
import numpy as np

def calculate_sma(data, length=20):
    """Calculates the Simple Moving Average (SMA)."""
    return data['Close'].rolling(window=length).mean()

def calculate_rsi(data, length=14):
    """Calculates the Relative Strength Index (RSI)."""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
    rs = gain / loss
    rs.fillna(0, inplace=True)
    rsi = 100 - (100 / (1 + rs))
    return rsi

def build_master_dataset(price_dir='data/raw', sentiment_dir='data/processed', output_path='data/processed/final_dataset.csv'):
    """
    Merges price data with sentiment data, adds technical indicators,
    and creates the final dataset for model training.
    """
    print("Building master dataset...")
    price_files = [f for f in os.listdir(price_dir) if f.endswith('.NS.csv')]
    
    all_stocks_df = []

    for price_file in price_files:
        ticker = price_file.replace('.csv', '')
        print(f"--- Processing {ticker} ---")

        # 1. Load price data and convert columns to numbers
        price_df = pd.read_csv(os.path.join(price_dir, price_file))
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            price_df[col] = pd.to_numeric(price_df[col], errors='coerce')
        price_df.dropna(subset=numeric_cols, inplace=True)
        price_df['Date'] = pd.to_datetime(price_df['Date']).dt.date

        # --- CORRECTED LOGIC ---
        # 2. Calculate technical indicators on the FULL price history
        price_df['SMA_20'] = calculate_sma(price_df)
        price_df['RSI_14'] = calculate_rsi(price_df)
        
        # 3. Load sentiment data
        sentiment_file = f"{ticker}_sentiment.csv"
        sentiment_path = os.path.join(sentiment_dir, sentiment_file)
        if not os.path.exists(sentiment_path):
            print(f"Warning: Sentiment file not found for {ticker}. Skipping.")
            continue
        sentiment_df = pd.read_csv(sentiment_path)
        sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date

        # 4. Merge the price_df (now with indicators) with the sentiment_df
        df = pd.merge(price_df, sentiment_df, left_on='Date', right_on='date', how='inner')
        df = df.drop(columns=['date']).set_index('Date')
        # --- END OF CORRECTION ---
        
        # 5. Create the Target Variable (Up or Down)
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        
        df['Ticker'] = ticker
        
        all_stocks_df.append(df)

    if not all_stocks_df:
        print("\n❌ Error: No data was successfully processed for any stock.")
        return

    final_df = pd.concat(all_stocks_df)
    final_df.dropna(inplace=True) # This will now only drop a few rows
    
    final_df.to_csv(output_path)
    print(f"\nFinal dataset shape: {final_df.shape}")
    print(f"✅ Master dataset created successfully at {output_path}")

if __name__ == '__main__':
    build_master_dataset()