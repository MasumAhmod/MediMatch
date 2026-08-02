import numpy as np

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
from catboost import CatBoostClassifier

from preprocess import load_data


# Load Dataset
doctorData, PatientData = load_data()

# Features and Target
X = PatientData.drop(columns=["diseases"])
y = PatientData["diseases"]

# Encode Target Labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# 5-Fold Stratified Cross Validation
skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

# Models to Compare
models = [

    (
        "Decision Tree",
        DecisionTreeClassifier(
            random_state=42
        )
    ),

    (
        "Random Forest",
        RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            n_jobs=-1
        )
    ),

    (
        "Logistic Regression",
        LogisticRegression(
            max_iter=1000
        )
    ),

    (
        "Linear SVM",
        LinearSVC(
            random_state=42,
            max_iter=10000
        )
    ),

    (
        "XGBoost",
        XGBClassifier(
            random_state=42,
            eval_metric="mlogloss"
        )
    ),

    (
        "CatBoost",
        CatBoostClassifier(
            iterations=100,
            learning_rate=0.1,
            depth=6,
            loss_function="MultiClass",
            random_seed=42,
            verbose=0,
            allow_writing_files=False
        )
    )

]

print("=" * 65)
print("5-Fold Stratified Cross Validation")
print("=" * 65)

results = []

for name, model in models:

    scores = cross_val_score(
        estimator=model,
        X=X,
        y=y,
        cv=skf,
        scoring="accuracy",
        n_jobs=-1
    )

    print(f"\n{name}")
    print("-" * 40)

    for i, score in enumerate(scores, start=1):
        print(f"Fold {i}: {score:.4f}")

    print("-" * 40)
    print(f"Average Accuracy : {np.mean(scores):.4f}")
    print(f"Std Deviation    : {np.std(scores):.4f}")

    results.append(
        (
            name,
            np.mean(scores),
            np.std(scores)
        )
    )

print("\n")
print("=" * 65)
print("Summary")
print("=" * 65)

results.sort(key=lambda x: x[1], reverse=True)

for model_name, mean_acc, std_acc in results:
    print(
        f"{model_name:<22}"
        f" Accuracy: {mean_acc:.4f}"
        f"   Std: {std_acc:.4f}"
    )