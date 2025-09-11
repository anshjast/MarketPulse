import pandas as pd
import os
import numpy as np

# --- (Keep your existing SMA and RSI functions here) ---
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

# --- NEW FUNCTIONS TO ADD ---
def calculate_macd(data, slow=26, fast=12, signal=9):
    """Calculates the Moving Average Convergence Divergence (MACD)."""
    exp1 = data['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = data['Close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

def calculate_bbands(data, length=20, std_dev=2):
    """Calculates Bollinger Bands."""
    sma = data['Close'].rolling(window=length).mean()
    std = data['Close'].rolling(window=length).std()
    upper_band = sma + (std * std_dev)
    lower_band = sma - (std * std_dev)
    return upper_band, lower_band

def build_master_dataset(price_dir='data/raw', sentiment_dir='data/processed', output_path='data/processed/final_dataset.csv'):
    print("Building master dataset with new features...")
    price_files = [f for f in os.listdir(price_dir) if f.endswith('.NS.csv')]
    
    all_stocks_df = []

    for price_file in price_files:
        ticker = price_file.replace('.csv', '')
        print(f"--- Processing {ticker} ---")

        price_df = pd.read_csv(os.path.join(price_dir, price_file))
        numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in numeric_cols:
            price_df[col] = pd.to_numeric(price_df[col], errors='coerce')
        price_df.dropna(subset=numeric_cols, inplace=True)
        price_df['Date'] = pd.to_datetime(price_df['Date']).dt.date

        # Calculate indicators on the FULL price history
        price_df['SMA_20'] = calculate_sma(price_df)
        price_df['RSI_14'] = calculate_rsi(price_df)
        
        # --- ADD NEW INDICATOR CALCULATIONS ---
        price_df['MACD'], price_df['MACD_Signal'] = calculate_macd(price_df)
        price_df['Upper_Band'], price_df['Lower_Band'] = calculate_bbands(price_df)
        
        # Load and merge sentiment data
        sentiment_file = f"{ticker}_sentiment.csv"
        sentiment_path = os.path.join(sentiment_dir, sentiment_file)
        if not os.path.exists(sentiment_path): continue
        sentiment_df = pd.read_csv(sentiment_path)
        sentiment_df['date'] = pd.to_datetime(sentiment_df['date']).dt.date
        
        df = pd.merge(price_df, sentiment_df, left_on='Date', right_on='date', how='inner')
        df = df.drop(columns=['date']).set_index('Date')
        
        # Create Target and Ticker columns
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        df['Ticker'] = ticker
        
        all_stocks_df.append(df)

    final_df = pd.concat(all_stocks_df)
    final_df.dropna(inplace=True)
    
    final_df.to_csv(output_path)
    print(f"\nFinal dataset shape: {final_df.shape}")
    print(f"✅ Master dataset created successfully at {output_path}")

if __name__ == '__main__':
    build_master_dataset()