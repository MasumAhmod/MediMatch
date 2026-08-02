import joblib
from pathlib import Path


# Model Directory
MODEL_DIR = Path(__file__).parent

# Load Trained CatBoost Model
model = joblib.load(
    MODEL_DIR / "catboost.pkl"
)

# Load Label Encoder
label_encoder = joblib.load(
    MODEL_DIR / "label_encoder.pkl"
)


def predict_disease(symptoms):
    """
    Predict disease from symptom vector.

    Parameters:
        symptoms (list): A list of symptom values (0/1).

    Returns:
        str: Predicted disease name.
    """

    # Predict encoded disease label
    prediction = model.predict([symptoms])

    # Convert shape (1,1) -> (1,)
    prediction = prediction.ravel().astype(int)

    # Decode label back to disease name
    disease = label_encoder.inverse_transform(prediction)

    return disease[0]