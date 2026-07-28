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


doctorData, PatientData = load_data()

X_train, X_test, y_train, y_test = preprocess_patient_data(PatientData)


MODEL_DIR = Path(__file__).parent

models = {
    "Decision Tree":
        joblib.load(MODEL_DIR / "decision_tree.pkl"),

    "Random Forest":
        joblib.load(MODEL_DIR / "random_forest.pkl"),

    "Logistic Regression":
        joblib.load(MODEL_DIR / "logistic_regression.pkl")
}

results = []

for name, model in models.items():

    pred = model.predict(X_test)

    results.append({

        "Model": name,

        "Accuracy":
            accuracy_score(y_test, pred),

        "Precision":
            precision_score(
                y_test,
                pred,
                average="weighted"
            ),

        "Recall":
            recall_score(
                y_test,
                pred,
                average="weighted"
            ),

        "F1-score":
            f1_score(
                y_test,
                pred,
                average="weighted"
            )
    })

    print("=" * 60)
    print(name)
    print("=" * 60)

    print(classification_report(y_test, pred))


results_df = pd.DataFrame(results)

print(results_df)

results_df.to_csv(
    MODEL_DIR / "model_comparison.csv",
    index=False
)