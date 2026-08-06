import joblib
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent

model = joblib.load(MODEL_DIR / "catboost.pkl")
label_encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")

FEATURE_NAMES = model.feature_names_


def predict_disease(selected_symptoms: list[str]):
    """
    Predict disease from symptom names.

    Example:
        ["fever", "cough", "fatigue"]
    """

    # Create dictionary with every symptom = 0
    symptom_vector = {
        feature: 0
        for feature in FEATURE_NAMES
    }

    # Validate symptoms
    invalid_symptoms = []

    for symptom in selected_symptoms:

        symptom = symptom.strip()

        if symptom in symptom_vector:
            symptom_vector[symptom] = 1
        else:
            invalid_symptoms.append(symptom)

    if invalid_symptoms:
        raise ValueError(
            f"Unknown symptom(s): {', '.join(invalid_symptoms)}"
        )

    # Convert to DataFrame
    X = pd.DataFrame([symptom_vector])

    prediction = model.predict(X)

    prediction = prediction.ravel().astype(int)

    disease = label_encoder.inverse_transform(prediction)

    return disease[0]