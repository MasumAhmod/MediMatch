import joblib
from pathlib import Path


MODEL_DIR = Path(__file__).parent


# ---------------------------------------------------------
# Load model
# ---------------------------------------------------------

model = joblib.load(
    MODEL_DIR / "catboost.pkl"
)


# ---------------------------------------------------------
# Load label encoder
# ---------------------------------------------------------

label_encoder = joblib.load(
    MODEL_DIR / "label_encoder.pkl"
)


# ---------------------------------------------------------
# Get model symptoms
# ---------------------------------------------------------

MODEL_FEATURES = model.feature_names_


# ---------------------------------------------------------
# Disease prediction
# ---------------------------------------------------------

def predict_disease(symptoms: list[str]):
    """
    Predict disease from symptom names.
    """

    # Normalize input symptoms
    symptoms = [
        symptom.strip().lower()
        for symptom in symptoms
    ]

    # Create a binary feature vector
    feature_vector = [
        1 if feature.lower() in symptoms else 0
        for feature in model.feature_names_
    ]

    # Predict disease
    prediction = model.predict([feature_vector])

    prediction = prediction.ravel().astype(int)

    # Decode disease label
    disease = label_encoder.inverse_transform(prediction)

    return disease[0]