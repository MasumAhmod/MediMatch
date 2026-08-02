import joblib
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from preprocess import load_data, preprocess_patient_data


# Load Dataset
doctorData, PatientData = load_data()

# Split Dataset
X_train, X_test, y_train, y_test = preprocess_patient_data(PatientData)

# Model Directory
MODEL_DIR = Path(__file__).parent

# Load Trained Model
model = joblib.load(
    MODEL_DIR / "catboost.pkl"
)

# Load Label Encoder
label_encoder = joblib.load(
    MODEL_DIR / "label_encoder.pkl"
)

# Encode Test Labels
y_test_encoded = label_encoder.transform(y_test)

# Predict
pred = model.predict(X_test)

# Convert predictions from (n,1) -> (n,)
pred = pred.ravel().astype(int)

# Evaluation Metrics
print("=" * 50)
print("CatBoost Model Evaluation")
print("=" * 50)

print(f"Accuracy : {accuracy_score(y_test_encoded, pred):.4f}")

print(
    f"Precision: {precision_score(y_test_encoded, pred, average='weighted'):.4f}"
)

print(
    f"Recall   : {recall_score(y_test_encoded, pred, average='weighted'):.4f}"
)

print(
    f"F1-score : {f1_score(y_test_encoded, pred, average='weighted'):.4f}"
)

print("\nClassification Report")
print("=" * 50)

print(
    classification_report(
        y_test_encoded,
        pred,
        target_names=label_encoder.classes_
    )
)