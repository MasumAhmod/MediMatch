import joblib
from pathlib import Path

MODEL_DIR = Path(__file__).parent

model = joblib.load(MODEL_DIR / "logistic_regression.pkl")


def predict_disease(symptoms):

    prediction = model.predict([symptoms])

    return prediction[0]