from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import shap
from typing import List, Dict
import os

app = FastAPI(title="People Analytics - Turnover Prediction API")

# Carregar artefatos
MODEL_PATH = os.getenv("MODEL_PATH", "../models/turnover_rf_model.pkl")
SCALER_PATH = os.getenv("SCALER_PATH", "../models/scaler.pkl")
FEATURES_PATH = os.getenv("FEATURES_PATH", "../models/feature_names.pkl")

model = joblib.load(MODEL_PATH) if os.path.exists(MODEL_PATH) else None
scaler = joblib.load(SCALER_PATH) if os.path.exists(SCALER_PATH) else None
feature_names = joblib.load(FEATURES_PATH) if os.path.exists(FEATURES_PATH) else []
explainer = shap.TreeExplainer(model) if model else None

class PredictionRequest(BaseModel):
    satisfacao_media: float
    satisfacao_std: float
    recompensa_media: float
    recompensa_std: float
    gestor_media: float
    gestor_std: float
    wlb_media: float
    wlb_std: float
    ambiente_media: float
    ambiente_std: float
    red_flag_count: int
    yellow_flag_count: int
    interaction_gestor_recompensa: float
    interaction_wlb_satisfacao: float
    cargo_encoded: int
    age_encoded: int
    tenure_normalized: float

class PredictionResponse(BaseModel):
    risk_score: float
    risk_level: str
    top_drivers: List[Dict[str, float]]
    suggested_actions: List[str]

@app.get("/health")
def health_check():
    return {"status": "OK", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if model is None or scaler is None or not feature_names:
        raise HTTPException(status_code=503, detail="Modelo não carregado. Treine e salve os artefatos em /models.")

    X = pd.DataFrame([request.dict()], columns=feature_names)
    X_scaled = scaler.transform(X)

    y_proba = model.predict_proba(X_scaled)[0]
    risk_score = float(y_proba[1])

    risk_level = 'BAIXO' if risk_score < 0.3 else ('MÉDIO' if risk_score < 0.7 else 'ALTO')

    shap_values = explainer.shap_values(X_scaled)
    shap_values_class1 = shap_values[1] if isinstance(shap_values, list) else shap_values
    top_indices = np.argsort(np.abs(shap_values_class1[0]))[-3:][::-1]
    top_drivers = [
        {"feature": feature_names[i], "shap_value": float(shap_values_class1[0][i])}
        for i in top_indices
    ]

    actions = suggest_actions(request.dict(), risk_score)

    return PredictionResponse(
        risk_score=risk_score,
        risk_level=risk_level,
        top_drivers=top_drivers,
        suggested_actions=actions
    )


def suggest_actions(features: Dict, risk_score: float) -> List[str]:
    actions = []
    if features['gestor_media'] < 2.5 and risk_score > 0.5:
        actions.append('Avaliar relacionamento com gestor')
    if features['recompensa_media'] < 2.5 and risk_score > 0.5:
        actions.append('Revisar salário/benefícios')
    if features['wlb_media'] < 2.5 and risk_score > 0.5:
        actions.append('Considerar redução de horas ou realocação')
    if features['red_flag_count'] > 5:
        actions.append('Conversa de retenção urgente')
    if risk_score > 0.7:
        actions.append('Envolver RH Partner e liderança')
    return actions if actions else ['Monitorar regularmente']
