from fastapi import FastAPI
from fastapi import HTTPException
import numpy as np
import pandas as pd
from app.schemas import PredictionRequest, PredictionResponse
from app.model_loader import feature_cols, model, threshold

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/ready")
def readiness_check():
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded.")
    if feature_cols is None or len(feature_cols) == 0:
        raise HTTPException(status_code=503, detail="Feature columns are not loaded.")
    return {"status": "ready", "n_features": len(feature_cols)}

@app.post("/predict")
def predict(request: PredictionRequest):
    x = np.asarray(request.features, dtype=float)

    if feature_cols is not None and len(x) != len(feature_cols):
        raise HTTPException(
            status_code=422,
            detail=f"Expected {len(feature_cols)} features but got {len(x)}.",
        )

    if feature_cols is None:
        X = x.reshape(1, -1)
    else:
        X = pd.DataFrame([x], columns=feature_cols)

    proba = model.predict_proba(X)[0, 1]
    pred = int(proba >= threshold)
    return PredictionResponse(
        probability=float(proba),
        prediction=pred,
    )