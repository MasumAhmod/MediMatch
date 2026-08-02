import joblib
from pathlib import Path

from catboost import CatBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

from preprocess import load_data, preprocess_patient_data


# Load Dataset
doctorData, PatientData = load_data()

# Preprocess Dataset
X_train, X_test, y_train, y_test = preprocess_patient_data(PatientData)

# Encode Disease Labels
label_encoder = LabelEncoder()

y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# Train CatBoost Model
cat_model = CatBoostClassifier(
    iterations=500,
    learning_rate=0.1,
    depth=6,
    loss_function="MultiClass",
    random_seed=42,
    verbose=0,
    allow_writing_files=False
)

cat_model.fit(X_train, y_train_encoded)

# Predict on Test Set
pred = cat_model.predict(X_test)

# Convert predictions from shape (n,1) to (n,)
pred = pred.ravel().astype(int)

# Testing Accuracy
print("Testing Accuracy:", accuracy_score(y_test_encoded, pred))

# Save Model and Label Encoder
MODEL_DIR = Path(__file__).parent

joblib.dump(
    cat_model,
    MODEL_DIR / "catboost.pkl"
)

joblib.dump(
    label_encoder,
    MODEL_DIR / "label_encoder.pkl"
)

print("\nCatBoost model trained successfully.")
print("Model saved as catboost.pkl")
print("Label encoder saved as label_encoder.pkl")