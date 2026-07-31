import joblib
import pandas as pd
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from preprocess import load_data, preprocess_patient_data

# Load data
doctorData, PatientData = load_data()
X_train, X_test, y_train, y_test = preprocess_patient_data(PatientData)

# Load encoder
MODEL_DIR = Path(__file__).parent
label_encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")

# Encode test labels
y_test_encoded = label_encoder.transform(y_test)

# Load models
models = {
    "Decision Tree": joblib.load(MODEL_DIR / "decision_tree.pkl"),
    "Random Forest": joblib.load(MODEL_DIR / "random_forest.pkl"),
    "Logistic Regression": joblib.load(MODEL_DIR / "logistic_regression.pkl"),
    "Linear SVM": joblib.load(MODEL_DIR / "linear_svm.pkl"),
    "XGBoost": joblib.load(MODEL_DIR / "xgboost.pkl"),
    "CatBoost": joblib.load(MODEL_DIR / "catboost.pkl"),
}

results = []

for name, model in models.items():

    pred = model.predict(X_test)

    if len(pred.shape) > 1:
        pred = pred.ravel()

    results.append({
        "Model": name,
        "Accuracy": accuracy_score(y_test_encoded, pred),
        "Precision": precision_score(
            y_test_encoded,
            pred,
            average="weighted",
            zero_division=0
        ),
        "Recall": recall_score(
            y_test_encoded,
            pred,
            average="weighted",
            zero_division=0
        ),
        "F1-score": f1_score(
            y_test_encoded,
            pred,
            average="weighted",
            zero_division=0
        )
    })

    print(f"\n{name}")
    print(classification_report(
        y_test_encoded,
        pred,
        zero_division=0
    ))

results_df = pd.DataFrame(results)

print(results_df)

results_df.to_csv(
    MODEL_DIR / "model_comparison.csv",
    index=False
)