import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "data", "globalterrorism.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")

ATTACK_MODEL_PATH = os.path.join(MODELS_DIR, "attack_prediction_model.pkl")
FEATURE_ENCODERS_PATH = os.path.join(MODELS_DIR, "feature_encoders.pkl")
TARGET_ENCODER_PATH = os.path.join(MODELS_DIR, "target_encoder.pkl")
SEVERITY_MODEL_PATH = os.path.join(MODELS_DIR, "severity_model.pkl")
SEVERITY_ENCODERS_PATH = os.path.join(MODELS_DIR, "severity_encoders.pkl")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")