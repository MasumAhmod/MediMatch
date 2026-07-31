import joblib
from pathlib import Path

from lightgbm import LGBMClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.preprocessing import LabelEncoder

from preprocess import load_data, preprocess_patient_data

doctorData, PatientData = load_data()

X_train, X_test, y_train, y_test = preprocess_patient_data(PatientData)
label_encoder = LabelEncoder()

y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

print("TRAIN.PY IS RUNNING")
# Decision Tree
dt = DecisionTreeClassifier(random_state = 42)
dt.fit(X_train, y_train_encoded)

# Random Forest
rf = RandomForestClassifier(
    n_estimators = 100,
    max_depth = 20,
    random_state = 42,
    n_jobs = -1
)

rf.fit(X_train, y_train_encoded)

# Logistic Regression
lr = LogisticRegression(max_iter = 1000)

lr.fit(X_train, y_train_encoded)

# Linear SVM
svm = LinearSVC(
    random_state = 42,
    max_iter = 10000
)

svm.fit(X_train, y_train_encoded)

# XGBoost
xgb = XGBClassifier(random_state = 42, eval_metric = 'mlogloss')
xgb.fit(X_train, y_train_encoded) 

#CatBoost
cat_model = CatBoostClassifier(
    iterations = 500,
    learning_rate = 0.1,
    depth = 6,
    loss_function = 'MultiClass',
    random_seed = 42,
    verbose = 0
)
cat_model.fit(X_train, y_train_encoded)


MODEL_DIR = Path(__file__).parent
joblib.dump(dt, MODEL_DIR / "decision_tree.pkl")
joblib.dump(rf, MODEL_DIR / "random_forest.pkl")
joblib.dump(lr, MODEL_DIR / "logistic_regression.pkl")
joblib.dump(svm, MODEL_DIR / "linear_svm.pkl")
joblib.dump(xgb, MODEL_DIR / "xgboost.pkl")
joblib.dump(cat_model, MODEL_DIR / "catboost.pkl")
joblib.dump(label_encoder, MODEL_DIR / "label_encoder.pkl")