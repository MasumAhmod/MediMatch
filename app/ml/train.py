import joblib
from pathlib import Path

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from preprocess import load_data, preprocess_patient_data

doctorData, PatientData = load_data()

X_train, X_test, y_train, y_test = preprocess_patient_data(PatientData)


# Decision Tree
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train, y_train)

# Random Forest
rf = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

rf.fit(X_train, y_train)

# Logistic Regression
lr = LogisticRegression(max_iter=1000)

lr.fit(X_train, y_train)


MODEL_DIR = Path(__file__).parent

joblib.dump(dt, MODEL_DIR / "decision_tree.pkl")
joblib.dump(rf, MODEL_DIR / "random_forest.pkl")
joblib.dump(lr, MODEL_DIR / "logistic_regression.pkl")

print("Models trained and saved successfully.")