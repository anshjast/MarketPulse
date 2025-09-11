import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_classification_model(data_path='data/processed/final_dataset.csv', model_output_path='models/marketpulse_classifier.joblib'):
    """
    Loads the final dataset, trains an XGBoost classifier, and evaluates its performance.
    """
    print("--- Starting Model Training ---")

    df = pd.read_csv(data_path, index_col='Date', parse_dates=True)

    features = [
    'Open', 'High', 'Low', 'Close', 'Volume', 'sentiment_score', 
    'SMA_20', 'RSI_14', 'MACD', 'MACD_Signal', 'Upper_Band', 'Lower_Band'
    ]
    target = 'Target'

    X = df[features]
    y = df[target]

   
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training on {len(X_train)} samples, testing on {len(X_test)} samples.")

    model = xgb.XGBClassifier(
        objective='binary:logistic',
        n_estimators=1000,
        learning_rate=0.01,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42,
        n_jobs=-1
    )
    
    print("Training the model... (This might take a minute)")
    model.fit(X_train, y_train)

    print("\n--- Model Evaluation on Test Data ---")
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"Model Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, target_names=['Down/Same', 'Up']))

    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(model, model_output_path)
    print(f"\n✅ Model saved successfully to {model_output_path}")

if __name__ == '__main__':
    train_classification_model()