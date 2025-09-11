import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_classification_model(data_path='data/processed/final_dataset.csv', model_output_path='models/marketpulse_classifier.joblib'):
    """
    Loads the final dataset, performs hyperparameter tuning, trains the best
    XGBoost classifier, and evaluates its performance.
    """
    print("--- Starting Model Training with Hyperparameter Tuning ---")

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

    print("\n--- Starting Hyperparameter Tuning ---")

    param_grid = {
        'n_estimators': [100, 300, 500, 1000],
        'max_depth': [3, 5, 7, 10],
        'learning_rate': [0.01, 0.05, 0.1],
        'gamma': [0, 0.1, 0.2],
        'subsample': [0.7, 0.8, 0.9, 1.0],
        'colsample_bytree': [0.7, 0.8, 0.9, 1.0]
    }

    model = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        use_label_encoder=False,
        random_state=42
    )
    random_search = RandomizedSearchCV(
        model, 
        param_distributions=param_grid,
        n_iter=50,
        cv=5,
        scoring='accuracy',
        n_jobs=-1,
        random_state=42,
        verbose=1 
    )

    random_search.fit(X_train, y_train)

    print("\n--- Hyperparameter Tuning Complete ---")
    print(f"Best Parameters Found: {random_search.best_params_}")
    
    best_model = random_search.best_estimator_

    print("\n--- Final Model Evaluation on Test Data ---")
    predictions = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    print(f"Tuned Model Accuracy: {accuracy:.2%}")
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, target_names=['Down/Same', 'Up']))

    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    joblib.dump(best_model, model_output_path)
    print(f"\n✅ Best model saved successfully to {model_output_path}")

if __name__ == '__main__':
    train_classification_model()