import joblib
from pathlib import Path


# =========================================================
# MODEL DIRECTORY
# =========================================================

MODEL_DIR = Path(__file__).parent


# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load(
    MODEL_DIR / "catboost.pkl"
)


# =========================================================
# LOAD LABEL ENCODER
# =========================================================

label_encoder = joblib.load(
    MODEL_DIR / "label_encoder.pkl"
)


# =========================================================
# MODEL FEATURES
# =========================================================

MODEL_FEATURES = model.feature_names_


# =========================================================
# DISEASE PREDICTION
# =========================================================

def predict_disease(symptoms: list[str]) -> str:
    """
    Predict disease from a list of symptom names.
    """

    # -----------------------------------------------------
    # Normalize symptoms
    # -----------------------------------------------------

    normalized_symptoms: set[str] = {
        symptom.strip().lower()
        for symptom in symptoms
        if symptom.strip()
    }


    # -----------------------------------------------------
    # Create binary feature vector
    # -----------------------------------------------------

    feature_vector = [
        1 if feature.strip().lower() in normalized_symptoms else 0
        for feature in MODEL_FEATURES
    ]


    # -----------------------------------------------------
    # Predict disease
    # -----------------------------------------------------

    prediction = model.predict([feature_vector])


    # -----------------------------------------------------
    # Convert prediction to integer
    # -----------------------------------------------------

    prediction = prediction.ravel().astype(int)


    # -----------------------------------------------------
    # Decode disease label
    # -----------------------------------------------------

    disease = label_encoder.inverse_transform(prediction)


    return str(disease[0])