import joblib

model_bundle = joblib.load("models/rf_sex.joblib")

if isinstance(model_bundle, dict):
    model = model_bundle["model"]
    threshold = model_bundle.get("threshold", 0.5)
    feature_cols = model_bundle.get("feature_cols")
else:
    model = model_bundle
    threshold = 0.5
    feature_cols = None



