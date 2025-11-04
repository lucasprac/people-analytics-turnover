"""
Treina Random Forest e salva artefatos
"""
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import joblib
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres123@localhost:5432/people_analytics')


def load_data():
    engine = create_engine(DATABASE_URL)
    df = pd.read_sql('SELECT * FROM processed_features', engine)
    return df


def prepare(df: pd.DataFrame):
    y = df['target']
    drop_cols = [c for c in ['target','response_id','employee_id','created_at'] if c in df.columns]
    X = df.drop(columns=drop_cols).fillna(df.mean(numeric_only=True))
    scaler = StandardScaler()
    Xs = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    return Xs, y, scaler


def split(X, y):
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def balance(X_train, y_train):
    sm = SMOTE(random_state=42)
    return sm.fit_resample(X_train, y_train)


def tune(X_train, y_train):
    grid = {
        'n_estimators': [100, 200],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'max_features': ['sqrt', 'log2'],
    }
    gs = GridSearchCV(RandomForestClassifier(random_state=42, n_jobs=-1, class_weight='balanced'),
                      grid, cv=5, scoring='f1', n_jobs=-1, verbose=1)
    gs.fit(X_train, y_train)
    return gs.best_estimator_


def evaluate(model, X_train, X_test, y_train, y_test):
    y_pred = model.predict(X_test)
    proba = model.predict_proba(X_test)[:,1]
    print(classification_report(y_test, y_pred))
    print(confusion_matrix(y_test, y_pred))
    auc = roc_auc_score(y_test, proba)
    fpr, tpr, _ = roc_curve(y_test, proba)
    os.makedirs('docs', exist_ok=True)
    plt.figure(figsize=(8,6))
    plt.plot(fpr, tpr, label=f'AUC={auc:.2f}')
    plt.plot([0,1],[0,1],'k--')
    plt.xlabel('FPR'); plt.ylabel('TPR'); plt.title('ROC Curve')
    plt.legend(); plt.tight_layout()
    plt.savefig('docs/roc_curve.png', dpi=200)
    print('Saved docs/roc_curve.png')


def save(model, scaler, X_train):
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/turnover_rf_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(list(X_train.columns), 'models/feature_names.pkl')


def main():
    df = load_data()
    X, y, scaler = prepare(df)
    X_train, X_test, y_train, y_test = split(X, y)
    Xb, yb = balance(X_train, y_train)
    model = tune(Xb, yb)
    evaluate(model, Xb, X_test, yb, y_test)
    save(model, scaler, X)
    print('Model and artifacts saved in /models')


if __name__ == '__main__':
    main()
